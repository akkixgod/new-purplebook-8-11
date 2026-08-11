#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for PurpleBook test 7 (ElitePractice X7)."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/purplebook-test-7/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Georgia, serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def table_svg(
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[int],
    *,
    font_size: int = 12,
    header_font: int = 11,
    row_h: int | None = None,
    header_h: int | None = None,
) -> str:
    """Table helper. Use '|' in a header cell for a two-line header."""
    widths = col_widths
    width = sum(widths) + 40
    needs_wrap = any("|" in h for h in headers)
    hh = header_h if header_h is not None else (48 if needs_wrap else 36)
    rh = row_h if row_h is not None else 36
    title_h = 56 if title else 16
    height = title_h + 16 + hh + rh * len(rows) + 16
    x0, y0 = 20, title_h
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{hh}" fill="#f3f4f6" stroke="#111"/>'
        )
        if "|" in h:
            lines = h.split("|")
            line_h = 14
            start_y = y0 + (hh - line_h * (len(lines) - 1)) / 2 - 2
            for li, line in enumerate(lines):
                cells.append(
                    f'<text x="{x + widths[i] / 2}" y="{start_y + li * line_h}" text-anchor="middle" '
                    f'font-family="{FONT}" font-size="{header_font}" font-weight="700">{line}</text>'
                )
        else:
            cells.append(
                f'<text x="{x + widths[i] / 2}" y="{y0 + hh / 2 + 4}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="{header_font}" font-weight="700">{h}</text>'
            )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + hh + rh * r
        x = x0
        for i, cell in enumerate(row):
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{rh}" fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i] / 2}" y="{y + rh / 2 + 4}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="{font_size}">{cell}</text>'
            )
            x += widths[i]
    title_el = (
        f'<text x="{width / 2}" y="28" text-anchor="middle" font-family="{FONT}" '
        f'font-size="13" font-weight="700">{title}</text>'
        if title
        else ""
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {title_el}
  {"".join(cells)}
</svg>'''


def eng1_q11_hoards() -> str:
    return table_svg(
        "Examples of Hoards found in Ireland and Northern Ireland",
        ["Hoard name", "Date of contents", "Year of discovery", "Description"],
        [
            ["Carrick-on-Suir Hoard", "17th century CE", "2013", "gold coins"],
            ["Ardagh Hoard", "10th century CE", "1868", "silver and bronze pieces"],
            ["Balline Hoard", "4th century CE", "1940", "silver pieces"],
        ],
        [170, 130, 130, 170],
    )


def eng1_q12_lava_worlds() -> str:
    return table_svg(
        "Three Candidate Lava Worlds, by Modeled Mass, Density, and Surface Temperature",
        ["Planet", "Mass (Earth masses)", "Density ratio", "Temperature (kelvins)"],
        [
            ["HD 80653 b", "5.6", "7.4", "2,300"],
            ["Kepler 10 b", "3.6", "6.0", "2,130"],
            ["K2-265 b", "0.8", "7.1", "1,400"],
        ],
        [130, 150, 120, 160],
    )


def eng2_q11_oklahoma() -> str:
    return table_svg(
        "Contributions of Three Key Industries to Oklahoma Economy in 2017",
        [
            "Industry",
            "Approximate total|contribution by industry",
            "Number of people|employed by industry",
            "Average contribution|per employee by industry",
        ],
        [
            ["Accommodation/food services", "$5,242,100,000", "150,373", "$34,861"],
            ["Retail", "$10,738,800,000", "179,208", "$59,924"],
            ["Tribal economic activity", "$7,312,400,000", "51,674", "$141,510"],
        ],
        [190, 160, 150, 160],
        header_font=10,
        font_size=11,
        header_h=52,
        row_h=40,
    )


def eng2_q12_video_games() -> str:
    return table_svg(
        "Home Video Game Systems of the 1970s and 1980s",
        [
            "System",
            "Manufacturer",
            "System type",
            "Approximate number of|units sold worldwide",
        ],
        [
            ["ColecoVision", "Coleco", "console", "2,000,000"],
            ["Intellivision", "Mattel", "console", "3,000,000"],
            ["MSX", "ASCII Corp.", "computer", "4,000,000"],
            ["Game & Watch", "Nintendo", "handheld", "18,600,000"],
        ],
        [130, 120, 110, 180],
        header_h=48,
    )


def eng2_q13_bird_mass() -> str:
    return table_svg(
        "Bird Species by Average Mass",
        ["Common name", "Average mass (kg)", "Capable of flight?"],
        [
            ["Lesser rhea", "19.6", "No"],
            ["Dalmatian pelican", "11.5", "Yes"],
            ["Andean condor", "11.3", "Yes"],
            ["Northern cassowary", "44.0", "No"],
        ],
        [170, 150, 150],
    )


def eng2_q14_migration() -> str:
    return table_svg(
        "Reported Annual Travel Distances in Four Studies of Migrating Animal Populations",
        ["Species", "Continent", "Distance (km)", "Measurement method"],
        [
            ["Mongolian gazelle", "Asia", "600", "RTD"],
            ["Khulan", "Asia", "5,067", "GPS"],
            ["Caribou", "North America", "1,350", "RTD"],
            ["Plains zebra", "Africa", "2,356", "GPS"],
        ],
        [150, 130, 120, 150],
    )


def math1_q10_scatter() -> str:
    """Scatterplot with line of best fit; slope ≈ −0.84, intercept ≈ 11.2."""
    W, H = 480, 440
    pad_l, pad_r, pad_t, pad_b = 50, 40, 30, 50
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmax, ymax = 8.0, 16.0

    def sx(x: float) -> float:
        return pad_l + (x / xmax) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / ymax) * plot_h

    # Points approximate Bluebook scatter
    points = [
        (1.0, 10.5),
        (2.0, 9.5),
        (3.0, 9.0),
        (4.0, 8.0),
        (5.0, 6.8),
        (6.0, 6.2),
        (7.0, 5.5),
        (8.0, 4.8),
    ]
    # y = 11.2 − 0.84x
    intercept, slope = 11.2, -0.84

    parts: list[str] = []
    # light unit grid
    for i in range(0, 9):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" stroke="#e5e7eb"/>'
        )
    for j in range(0, 17):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l + plot_w}" y2="{sy(j)}" stroke="#e5e7eb"/>'
        )
    # axes
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    # axis labels
    for i in range(0, 9):
        parts.append(
            f'<text x="{sx(i)}" y="{pad_t + plot_h + 18}" text-anchor="middle" '
            f'font-family="Arial" font-size="12">{i}</text>'
        )
    for j in range(0, 17, 2):
        parts.append(
            f'<text x="{pad_l - 8}" y="{sy(j) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="12">{j}</text>'
        )
    # best-fit line across full plot
    y0 = intercept
    y8 = intercept + slope * 8
    parts.append(
        f'<line x1="{sx(0)}" y1="{sy(y0)}" x2="{sx(8)}" y2="{sy(y8)}" stroke="#111" stroke-width="2"/>'
    )
    dots = "".join(
        f'<circle cx="{sx(x)}" cy="{sy(y)}" r="4.5" fill="#111"/>' for x, y in points
    )
    parts.append(dots)
    parts.append(
        f'<text x="{pad_l + plot_w + 12}" y="{pad_t + plot_h + 4}" font-family="Arial" font-size="14" font-style="italic">x</text>'
        f'<text x="{pad_l - 6}" y="{pad_t - 6}" font-family="Arial" font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q21_freq_tables() -> str:
    """Four stacked Value|Frequency choice tables labeled A–D with circled letters."""
    opts = [
        ("A", [("60", "2"), ("70", "3"), ("80", "4"), ("90", "5")]),
        ("B", [("60", "6"), ("70", "3"), ("80", "3"), ("90", "6")]),
        ("C", [("60", "4"), ("70", "4"), ("80", "4"), ("90", "4")]),
        ("D", [("60", "5"), ("70", "4"), ("80", "4"), ("90", "5")]),
    ]
    col_w = 110
    row_h = 28
    header_h = 28
    table_h = header_h + row_h * 4
    gap = 28
    box_pad_x = 70
    box_pad_y = 16
    box_w = box_pad_x + col_w * 2 + 40
    box_h = table_h + box_pad_y * 2
    W = box_w + 40
    H = 20 + len(opts) * (box_h + gap) - gap + 20
    parts: list[str] = []

    for idx, (lab, rows) in enumerate(opts):
        by = 20 + idx * (box_h + gap)
        bx = 20
        # choice card
        parts.append(
            f'<rect x="{bx}" y="{by}" width="{box_w}" height="{box_h}" rx="10" ry="10" '
            f'fill="#fff" stroke="#9ca3af" stroke-width="1.5"/>'
        )
        # circled letter
        cx, cy = bx + 32, by + box_h / 2
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="#111" stroke-width="1.5"/>'
            f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" font-family="Arial" font-size="16" font-weight="700">{lab}</text>'
        )
        # table
        tx = bx + box_pad_x
        ty = by + box_pad_y
        headers = ["Value", "Frequency"]
        for c, h in enumerate(headers):
            x = tx + c * col_w
            parts.append(
                f'<rect x="{x}" y="{ty}" width="{col_w}" height="{header_h}" fill="#fff" stroke="#111"/>'
                f'<text x="{x + col_w / 2}" y="{ty + 19}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="13" font-weight="700">{h}</text>'
            )
        for r, (val, freq) in enumerate(rows):
            y = ty + header_h + r * row_h
            for c, cell in enumerate([val, freq]):
                x = tx + c * col_w
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{col_w}" height="{row_h}" fill="#fff" stroke="#111"/>'
                    f'<text x="{x + col_w / 2}" y="{y + 19}" text-anchor="middle" '
                    f'font-family="{FONT}" font-size="13">{cell}</text>'
                )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


FIGURES = {
    "eng1-q11-hoards-ireland.svg": eng1_q11_hoards,
    "eng1-q12-lava-worlds.svg": eng1_q12_lava_worlds,
    "eng2-q11-oklahoma-industries.svg": eng2_q11_oklahoma,
    "eng2-q12-video-game-systems.svg": eng2_q12_video_games,
    "eng2-q13-bird-mass.svg": eng2_q13_bird_mass,
    "eng2-q14-migration-distances.svg": eng2_q14_migration,
    "math1-q10-scatter-best-fit.svg": math1_q10_scatter,
    "math1-q21-frequency-tables.svg": math1_q21_freq_tables,
}


def main() -> None:
    for name, fn in FIGURES.items():
        write(name, fn())
    print(f"done {len(FIGURES)} purplebook-test-7 figures")


if __name__ == "__main__":
    main()
