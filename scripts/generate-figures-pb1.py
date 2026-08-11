#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for PurpleBook test 1 (ElitePractice X1)."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/purplebook-test-1/figures")
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
    font_size: int = 12,
) -> str:
    widths = col_widths or ([180] + [140] * (len(headers) - 1))
    width = sum(widths) + 40
    row_h = 36
    title_h = 56 if title else 16
    height = title_h + 40 + row_h * (1 + len(rows)) + 20
    x0, y0 = 20, title_h
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{row_h}" fill="#f3f4f6" stroke="#111"/>'
            f'<text x="{x + widths[i]/2}" y="{y0 + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="{font_size}" font-weight="700">{h}</text>'
        )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + row_h * (r + 1)
        x = x0
        for i, cell in enumerate(row):
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i]/2}" y="{y + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="{font_size}">{cell}</text>'
            )
            x += widths[i]
    title_el = (
        f'<text x="{width/2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="700">{title}</text>'
        if title
        else ""
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {title_el}
  {"".join(cells)}
</svg>'''


def wrapped_title_table(
    title_lines: list[str],
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[int],
    header_font: int = 11,
) -> str:
    widths = col_widths
    width = sum(widths) + 40
    row_h = 40
    title_h = 22 + 18 * len(title_lines)
    height = title_h + 16 + row_h * (1 + len(rows)) + 20
    x0, y0 = 20, title_h
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{row_h}" fill="#f3f4f6" stroke="#111"/>'
        )
        # allow simple two-line headers via |
        if "|" in h:
            a, b = h.split("|", 1)
            cells.append(
                f'<text x="{x + widths[i]/2}" y="{y0 + 16}" text-anchor="middle" font-family="Georgia, serif" font-size="{header_font}" font-weight="700">{a}</text>'
                f'<text x="{x + widths[i]/2}" y="{y0 + 32}" text-anchor="middle" font-family="Georgia, serif" font-size="{header_font}" font-weight="700">{b}</text>'
            )
        else:
            cells.append(
                f'<text x="{x + widths[i]/2}" y="{y0 + 25}" text-anchor="middle" font-family="Georgia, serif" font-size="{header_font}" font-weight="700">{h}</text>'
            )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + row_h * (r + 1)
        x = x0
        for i, cell in enumerate(row):
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i]/2}" y="{y + 26}" text-anchor="middle" font-family="Georgia, serif" font-size="12">{cell}</text>'
            )
            x += widths[i]
    titles = "".join(
        f'<text x="{width/2}" y="{20 + 18 * i}" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="700">{line}</text>'
        for i, line in enumerate(title_lines)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {titles}
  {"".join(cells)}
</svg>'''


def ice_cream_table() -> str:
    # Multi-header: Flavor | Type of topping → Sprinkles / No Sprinkles
    W, H = 520, 220
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <rect x="20" y="20" width="200" height="70" fill="#f3f4f6" stroke="#111"/>
  <rect x="220" y="20" width="280" height="35" fill="#f3f4f6" stroke="#111"/>
  <rect x="220" y="55" width="140" height="35" fill="#f3f4f6" stroke="#111"/>
  <rect x="360" y="55" width="140" height="35" fill="#f3f4f6" stroke="#111"/>
  <text x="120" y="60" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="700">Flavor of ice cream</text>
  <text x="360" y="42" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="700">Type of topping</text>
  <text x="290" y="78" text-anchor="middle" font-family="Georgia, serif" font-size="12" font-weight="700">Sprinkles</text>
  <text x="430" y="78" text-anchor="middle" font-family="Georgia, serif" font-size="12" font-weight="700">No Sprinkles</text>
  <!-- rows -->
  <rect x="20" y="90" width="200" height="36" fill="#fff" stroke="#111"/>
  <rect x="220" y="90" width="140" height="36" fill="#fff" stroke="#111"/>
  <rect x="360" y="90" width="140" height="36" fill="#fff" stroke="#111"/>
  <text x="30" y="114" font-family="Georgia, serif" font-size="13">Chocolate</text>
  <text x="290" y="114" text-anchor="middle" font-family="Georgia, serif" font-size="13">60</text>
  <text x="430" y="114" text-anchor="middle" font-family="Georgia, serif" font-size="13">30</text>
  <rect x="20" y="126" width="200" height="36" fill="#fff" stroke="#111"/>
  <rect x="220" y="126" width="140" height="36" fill="#fff" stroke="#111"/>
  <rect x="360" y="126" width="140" height="36" fill="#fff" stroke="#111"/>
  <text x="30" y="150" font-family="Georgia, serif" font-size="13">Vanilla</text>
  <text x="290" y="150" text-anchor="middle" font-family="Georgia, serif" font-size="13">20</text>
  <text x="430" y="150" text-anchor="middle" font-family="Georgia, serif" font-size="13">30</text>
  <rect x="20" y="162" width="200" height="36" fill="#fff" stroke="#111"/>
  <rect x="220" y="162" width="140" height="36" fill="#fff" stroke="#111"/>
  <rect x="360" y="162" width="140" height="36" fill="#fff" stroke="#111"/>
  <text x="30" y="186" font-family="Georgia, serif" font-size="13">Twist</text>
  <text x="290" y="186" text-anchor="middle" font-family="Georgia, serif" font-size="13">80</text>
  <text x="430" y="186" text-anchor="middle" font-family="Georgia, serif" font-size="13">20</text>
</svg>'''


def parallels_m1q2() -> str:
    # r top, s bottom, t down-right; 103°/77° above r; 77° below-left at s; a° above-right at s (=77°)
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="320" viewBox="0 0 460 320">
  <rect width="100%" height="100%" fill="#fff"/>
  <line x1="40" y1="90" x2="400" y2="90" stroke="#111" stroke-width="2"/>
  <line x1="40" y1="210" x2="400" y2="210" stroke="#111" stroke-width="2"/>
  <line x1="120" y1="40" x2="300" y2="260" stroke="#111" stroke-width="2"/>
  <text x="410" y="95" font-family="Arial" font-size="16" font-style="italic">r</text>
  <text x="410" y="215" font-family="Arial" font-size="16" font-style="italic">s</text>
  <text x="305" y="255" font-family="Arial" font-size="16" font-style="italic">t</text>
  <text x="125" y="78" font-family="Arial" font-size="15">103°</text>
  <text x="210" y="78" font-family="Arial" font-size="15">77°</text>
  <text x="250" y="198" font-family="Arial" font-size="15">a°</text>
  <text x="175" y="245" font-family="Arial" font-size="15">77°</text>
  <text x="230" y="300" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def parallels_m2q2() -> str:
    # r top, s bottom, k down-right; w/x above r; z/y below s
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="320" viewBox="0 0 460 320">
  <rect width="100%" height="100%" fill="#fff"/>
  <line x1="40" y1="95" x2="400" y2="95" stroke="#111" stroke-width="2"/>
  <line x1="40" y1="215" x2="400" y2="215" stroke="#111" stroke-width="2"/>
  <line x1="130" y1="40" x2="310" y2="270" stroke="#111" stroke-width="2"/>
  <text x="410" y="100" font-family="Arial" font-size="16" font-style="italic">r</text>
  <text x="410" y="220" font-family="Arial" font-size="16" font-style="italic">s</text>
  <text x="145" y="48" font-family="Arial" font-size="16" font-style="italic">k</text>
  <text x="135" y="82" font-family="Arial" font-size="15">w°</text>
  <text x="220" y="82" font-family="Arial" font-size="15">x°</text>
  <text x="185" y="252" font-family="Arial" font-size="15">z°</text>
  <text x="265" y="252" font-family="Arial" font-size="15">y°</text>
  <text x="230" y="300" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def histograms_m1q15() -> str:
    W, H = 420, 520
    pad_l, pad_r, pad_t, pad_b = 50, 30, 36, 40
    plot_w = W - pad_l - pad_r
    plot_h = 180
    bins = [15, 20, 25, 30, 35, 40, 45, 50]
    team_a = [0, 0, 25, 50, 25, 0, 0]  # bins 15-20 .. 45-50
    team_b = [30, 25, 15, 10, 15, 30, 25]

    def panel(title: str, freqs: list[int], top: int) -> str:
        parts = [
            f'<text x="{pad_l}" y="{top - 10}" font-family="Arial" font-size="14" font-weight="700">{title}</text>'
        ]
        for v in range(0, 51, 10):
            y = top + plot_h - (v / 50) * plot_h
            parts.append(
                f'<line x1="{pad_l}" y1="{y}" x2="{pad_l + plot_w}" y2="{y}" stroke="#e5e7eb"/>'
                f'<text x="{pad_l - 8}" y="{y + 4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>'
            )
        bw = plot_w / 7
        for i, f in enumerate(freqs):
            h = (f / 50) * plot_h
            x = pad_l + i * bw
            y = top + plot_h - h
            if f:
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" fill="#fff" stroke="#111" stroke-width="1.5"/>'
                )
        parts.append(
            f'<line x1="{pad_l}" y1="{top}" x2="{pad_l}" y2="{top + plot_h}" stroke="#111"/>'
            f'<line x1="{pad_l}" y1="{top + plot_h}" x2="{pad_l + plot_w}" y2="{top + plot_h}" stroke="#111"/>'
        )
        for i, lab in enumerate(bins):
            x = pad_l + i * (plot_w / 7)
            parts.append(
                f'<text x="{x}" y="{top + plot_h + 16}" text-anchor="middle" font-family="Arial" font-size="11">{lab}</text>'
            )
        parts.append(
            f'<text x="{pad_l + plot_w / 2}" y="{top + plot_h + 32}" text-anchor="middle" font-family="Arial" font-size="12">Score</text>'
            f'<text x="14" y="{top + plot_h / 2}" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-90 14 {top + plot_h / 2})">Frequency</text>'
        )
        return "\n".join(parts)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {panel("Team A", team_a, 40)}
  {panel("Team B", team_b, 300)}
</svg>'''


def pyramid_m2q10() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="340" viewBox="0 0 420 340">
  <rect width="100%" height="100%" fill="#fff"/>
  <path d="M 80,240 L 260,240 L 320,190 L 140,190 Z" fill="none" stroke="#111" stroke-width="2"/>
  <line x1="140" y1="190" x2="80" y2="240" stroke="#111" stroke-width="1.5" stroke-dasharray="5 4"/>
  <line x1="140" y1="190" x2="200" y2="60" stroke="#111" stroke-width="2"/>
  <line x1="320" y1="190" x2="200" y2="60" stroke="#111" stroke-width="2"/>
  <line x1="80" y1="240" x2="200" y2="60" stroke="#111" stroke-width="2"/>
  <line x1="260" y1="240" x2="200" y2="60" stroke="#111" stroke-width="2"/>
  <line x1="200" y1="60" x2="200" y2="215" stroke="#111" stroke-width="1.5" stroke-dasharray="5 4"/>
  <rect x="200" y="201" width="12" height="12" fill="none" stroke="#111"/>
  <text x="165" y="265" font-family="Arial" font-size="16" font-style="italic">l</text>
  <text x="295" y="225" font-family="Arial" font-size="16" font-style="italic">w</text>
  <text x="210" y="140" font-family="Arial" font-size="16" font-style="italic">h</text>
  <text x="210" y="320" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def line_m2q11() -> str:
    W, H = 420, 420
    pad = 40
    plot = 320

    def sx(x: float) -> float:
        return pad + ((x + 5) / 10) * plot

    def sy(y: float) -> float:
        return pad + ((5 - y) / 10) * plot

    grid = []
    for i in range(-5, 6):
        grid.append(f'<line x1="{sx(i)}" y1="{pad}" x2="{sx(i)}" y2="{pad+plot}" stroke="#e5e7eb"/>')
        grid.append(f'<line x1="{pad}" y1="{sy(i)}" x2="{pad+plot}" y2="{sy(i)}" stroke="#e5e7eb"/>')
        if i != 0:
            grid.append(
                f'<text x="{sx(i)}" y="{sy(0)+16}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>'
            )
            grid.append(
                f'<text x="{sx(0)-10}" y="{sy(i)+4}" text-anchor="end" font-family="Arial" font-size="11">{i}</text>'
            )
    # line y = 2x - 4 through visible window
    x1, x2 = -0.5, 4.5
    y1, y2 = 2 * x1 - 4, 2 * x2 - 4
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <line x1="{sx(0)}" y1="{pad}" x2="{sx(0)}" y2="{pad+plot}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad}" y1="{sy(0)}" x2="{pad+plot}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>
  <polygon points="{sx(0)},{pad-2} {sx(0)-5},{pad+10} {sx(0)+5},{pad+10}" fill="#111"/>
  <polygon points="{pad+plot+2},{sy(0)} {pad+plot-10},{sy(0)-5} {pad+plot-10},{sy(0)+5}" fill="#111"/>
  <text x="{pad+plot+8}" y="{sy(0)+4}" font-family="Arial" font-size="14" font-style="italic">x</text>
  <text x="{sx(0)+8}" y="{pad+12}" font-family="Arial" font-size="14" font-style="italic">y</text>
  <text x="{sx(0)+8}" y="{sy(0)+16}" font-family="Arial" font-size="12">O</text>
  <line x1="{sx(x1)}" y1="{sy(y1)}" x2="{sx(x2)}" y2="{sy(y2)}" stroke="#111" stroke-width="2.5"/>
</svg>'''


def main() -> None:
    write(
        "eng1-q09-pueblos.svg",
        table_svg(
            "Total Areas of Five Pueblo Nations in New Mexico",
            ["Tribal nation", "Area (square miles)"],
            [
                ["Pueblo of Acoma", "595.7"],
                ["Taos Pueblo", "156.2"],
                ["Pueblo of Sandia", "38.9"],
                ["Pueblo de Cochiti", "82.1"],
                ["Pueblo of Pojoaque", "21.4"],
            ],
            [240, 180],
        ),
    )
    write(
        "eng1-q10-tfa.svg",
        wrapped_title_table(
            [
                "Percent Change in Average Global Market Prices by",
                "Commodity in Two Agricultural Trade-Reform Scenarios",
            ],
            [
                "Commodity",
                "Percent change in|TFA scenario",
                "Percent change in|tariff-removal scenario",
            ],
            [
                ["Fruits and vegetables", "−1.50", "+0.04"],
                ["Processed foods", "−1.76", "−1.00"],
                ["Rice", "−0.37", "+1.36"],
                ["Wheat", "−1.35", "+0.45"],
            ],
            [180, 160, 200],
        ),
    )
    write(
        "eng1-q12-fruitflies.svg",
        wrapped_title_table(
            ["Monthly Temperatures and Wing Centroid Sizes of Fruit Fly Specimens"],
            [
                "Month",
                "Average high|(°F)",
                "Average low|(°F)",
                "Average male wing|centroid size (mm)",
                "Average female wing|centroid size (mm)",
            ],
            [
                ["October", "67", "44", "1.98", "2.29"],
                ["July", "87", "62", "2.02", "2.31"],
                ["June", "80", "56", "2.01", "2.31"],
                ["May", "73", "50", "1.98", "2.27"],
            ],
            [90, 100, 100, 150, 160],
            header_font=10,
        ),
    )
    write(
        "eng2-q11-strontium.svg",
        table_svg(
            "Strontium Isotope Ratios and Corresponding Numerical Ages in the Global Seawater Curve",
            ["⁸⁷Sr/⁸⁶Sr", "Age (Ma)"],
            [
                ["0.708980", "6.20"],
                ["0.709000", "5.86"],
                ["0.709020", "5.40"],
                ["0.709040", "4.75"],
                ["0.709060", "3.00"],
            ],
            [160, 140],
        ),
    )
    write("math1-q02-parallels.svg", parallels_m1q2())
    write("math1-q15-histograms.svg", histograms_m1q15())
    write("math1-q16-icecream.svg", ice_cream_table())
    write(
        "math1-q17-ages.svg",
        table_svg(
            "",
            ["Age group", "Proportion"],
            [
                ["Less than 18 years old", "34%"],
                ["18–40 years old", "23%"],
                ["41–65 years old", "22%"],
                ["Greater than 65 years old", "21%"],
            ],
            [260, 120],
        ),
    )
    write("math2-q02-parallels.svg", parallels_m2q2())
    write("math2-q10-pyramid.svg", pyramid_m2q10())
    write("math2-q11-line.svg", line_m2q11())
    write(
        "math2-q17-mail.svg",
        table_svg(
            "",
            ["Pieces of mail", "Days"],
            [
                ["0", "2"],
                ["4", "2"],
                ["5", "2"],
                ["6", "2"],
                ["7", "1"],
                ["8", "1"],
                ["17", "1"],
            ],
            [160, 100],
        ),
    )


if __name__ == "__main__":
    main()
