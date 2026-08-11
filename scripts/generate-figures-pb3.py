#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for PurpleBook test 3 (ElitePractice X3)."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/purplebook-test-3/figures")
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def table_svg(title: str, headers: list[str], rows: list[list[str]], col_widths: list[int]) -> str:
    widths = col_widths
    width = sum(widths) + 40
    row_h = 36
    title_h = 56 if title else 16
    height = title_h + 20 + row_h * (1 + len(rows)) + 16
    x0, y0 = 20, title_h
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{row_h}" fill="#f3f4f6" stroke="#111"/>'
            f'<text x="{x + widths[i]/2}" y="{y0 + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="11" font-weight="700">{h}</text>'
        )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + row_h * (r + 1)
        x = x0
        for i, cell in enumerate(row):
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i]/2}" y="{y + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="11">{cell}</text>'
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


def eng1_q10_tribal_nations() -> str:
    return table_svg(
        "Total Areas of Five Tribal Nations in California",
        ["Tribal nation", "Location", "Area (square miles)"],
        [
            ["Hoopa Valley Tribe", "Northern California", "141.68"],
            ["La Jolla Band of Luiseño Indians", "Southern California", "13.50"],
            ["Pauma Band of Luiseño Mission Indians", "Southern California", "9.36"],
            ["Agua Caliente Band of Cahuilla Indians", "Northern California", "53.68"],
            ["Los Coyotes Band of Cahuilla and Cupeño Indians", "Southern California", "39.21"],
        ],
        [220, 140, 120],
    )


def eng1_q13_urban_agriculture() -> str:
    W, H = 560, 380
    pad_l, pad_r, pad_t, pad_b = 70, 30, 80, 70
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    groups = ["project leaders", "stakeholders", "general public"]
    # biodiversity dark, microclimate light, attachment black
    data = {
        "biodiversity": [3.5, 4.1, 4.0],
        "microclimate": [3.0, 4.1, 3.8],
        "attachment": [3.0, 4.1, 4.4],
    }
    colors = {"biodiversity": "#6b7280", "microclimate": "#d1d5db", "attachment": "#111"}
    parts = [
        f'<text x="{W/2}" y="24" text-anchor="middle" font-family="Arial" font-size="12" font-weight="700">Rating (0 = no contribution, 5 = high contribution)</text>'
    ]
    for v in range(0, 6):
        y = pad_t + plot_h - (v / 5) * plot_h
        parts.append(
            f'<line x1="{pad_l}" y1="{y}" x2="{W-pad_r}" y2="{y}" stroke="#e5e7eb"/>'
            f'<text x="{pad_l-8}" y="{y+4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{H-pad_b}" stroke="#111"/>'
        f'<line x1="{pad_l}" y1="{H-pad_b}" x2="{W-pad_r}" y2="{H-pad_b}" stroke="#111"/>'
    )
    gw = plot_w / 3
    bw = gw * 0.22
    series = ["biodiversity", "microclimate", "attachment"]
    for gi, g in enumerate(groups):
        gx = pad_l + gi * gw
        for si, s in enumerate(series):
            val = data[s][gi]
            h = (val / 5) * plot_h
            x = gx + gw * 0.12 + si * (bw + 4)
            parts.append(
                f'<rect x="{x}" y="{pad_t + plot_h - h}" width="{bw}" height="{h}" fill="{colors[s]}" stroke="#111"/>'
            )
        parts.append(
            f'<text x="{gx + gw/2}" y="{H-pad_b+22}" text-anchor="middle" font-family="Arial" font-size="11">{g}</text>'
        )
    lx, ly = pad_l + 10, pad_t + 10
    labels = [
        ("increase in global biodiversity", "#6b7280"),
        ("improvement of local microclimate", "#d1d5db"),
        ("improvement of neighborhood attachment", "#111"),
    ]
    for i, (lab, col) in enumerate(labels):
        parts.append(
            f'<rect x="{lx}" y="{ly + i*18}" width="12" height="12" fill="{col}" stroke="#111"/>'
            f'<text x="{lx+18}" y="{ly + i*18 + 10}" font-family="Arial" font-size="10">{lab}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def eng1_q14_honeybee() -> str:
    W, H = 520, 340
    pad_l, pad_r, pad_t, pad_b = 60, 30, 70, 70
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    species = ["black dwarf\nhoneybee", "dwarf\nhoneybee", "western\nhoneybee"]
    data = {"5-sided": [2.5, 2.6, 0.5], "7-sided": [2.4, 2.1, 0.4], "8-sided": [0.0, 0.2, 0.1]}
    colors = {"5-sided": "#6b7280", "7-sided": "#d1d5db", "8-sided": "#111"}
    parts = [
        f'<text x="{W/2}" y="22" text-anchor="middle" font-family="Arial" font-size="12" font-weight="700">Percentage of Nonhexagonal Cells in Hives of Three Honeybee Species</text>',
        f'<text x="16" y="{(pad_t+H-pad_b)/2}" text-anchor="middle" font-family="Arial" font-size="11" transform="rotate(-90 16 {(pad_t+H-pad_b)/2})">Average percentage of nonhexagonal cells by shape</text>',
    ]
    y_max = 3.0
    for v in [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
        y = pad_t + plot_h - (v / y_max) * plot_h
        parts.append(
            f'<line x1="{pad_l}" y1="{y}" x2="{W-pad_r}" y2="{y}" stroke="#e5e7eb"/>'
            f'<text x="{pad_l-6}" y="{y+4}" text-anchor="end" font-family="Arial" font-size="10">{v:g}</text>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{H-pad_b}" stroke="#111"/>'
        f'<line x1="{pad_l}" y1="{H-pad_b}" x2="{W-pad_r}" y2="{H-pad_b}" stroke="#111"/>'
    )
    gw = plot_w / 3
    bw = gw * 0.22
    for gi in range(3):
        gx = pad_l + gi * gw
        for si, s in enumerate(["5-sided", "7-sided", "8-sided"]):
            val = data[s][gi]
            h = (val / y_max) * plot_h if val else 0
            x = gx + gw * 0.12 + si * (bw + 4)
            if h:
                parts.append(
                    f'<rect x="{x}" y="{pad_t + plot_h - h}" width="{bw}" height="{h}" fill="{colors[s]}" stroke="#111"/>'
                )
        parts.append(
            f'<text x="{gx + gw/2}" y="{H-pad_b+18}" text-anchor="middle" font-family="Arial" font-size="10">{species[gi].replace(chr(10)," ")}</text>'
        )
    lx, ly = W - 160, pad_t + 8
    for i, (s, col) in enumerate(colors.items()):
        parts.append(
            f'<rect x="{lx}" y="{ly + i*16}" width="10" height="10" fill="{col}" stroke="#111"/>'
            f'<text x="{lx+14}" y="{ly + i*16 + 9}" font-family="Arial" font-size="10">{s}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def eng2_q11_cougar() -> str:
    return table_svg(
        "Studies of Cougar Population Density",
        [
            "Study authors",
            "Location",
            "Methods",
            "Study area (square kilometers)",
            "Maximum density (cougars per 100 square kilometers)",
        ],
        [
            ["Ross Clarke", "British Columbia (Canada)", "Radio-collar tracking", "3,045", "0.72"],
            ["Veronica A. Quiroga et al.", "Argentina", "Regular camera trapping", "1,882", "1.26"],
            ["Richard A. Beausoleil et al.", "Washington (United States)", "biopsy darting", "7,939", "2.40"],
            ["David M. Choate et al.", "Utah (United States)", "Helicopter surveying", "1,300", "10.24"],
        ],
        [130, 120, 120, 100, 120],
    )


def math1_q08_bank_graph() -> str:
    W, H = 440, 360
    pad_l, pad_r, pad_t, pad_b = 70, 30, 30, 60
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    x0, x1, y0, y1 = 0, 10, 0, 80

    def sx(x: float) -> float:
        return pad_l + (x - x0) / (x1 - x0) * plot_w

    def sy(y: float) -> float:
        return pad_t + (y1 - y) / (y1 - y0) * plot_h

    parts = []
    for v in range(0, 81, 10):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(v)}" x2="{W-pad_r}" y2="{sy(v)}" stroke="#e5e7eb"/>'
            f'<text x="{pad_l-8}" y="{sy(v)+4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>'
        )
    for x in range(0, 11, 2):
        parts.append(
            f'<line x1="{sx(x)}" y1="{pad_t}" x2="{sx(x)}" y2="{H-pad_b}" stroke="#e5e7eb"/>'
            f'<text x="{sx(x)}" y="{H-pad_b+18}" text-anchor="middle" font-family="Arial" font-size="11">{x}</text>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{H-pad_b}" stroke="#111"/>'
        f'<line x1="{pad_l}" y1="{H-pad_b}" x2="{W-pad_r}" y2="{H-pad_b}" stroke="#111"/>'
    )
    # line from (0,35) to (10,55): slope 2
    parts.append(
        f'<line x1="{sx(0)}" y1="{sy(35)}" x2="{sx(10)}" y2="{sy(55)}" stroke="#111" stroke-width="2.5"/>'
    )
    parts.append(
        f'<circle cx="{sx(0)}" cy="{sy(35)}" r="4" fill="#111"/>'
        f'<circle cx="{sx(10)}" cy="{sy(55)}" r="4" fill="#111"/>'
    )
    parts.append(
        f'<text x="{(pad_l+W-pad_r)/2}" y="{H-8}" text-anchor="middle" font-family="Arial" font-size="12">Time since initial deposit (months)</text>'
        f'<text x="18" y="{(pad_t+H-pad_b)/2}" text-anchor="middle" font-family="Arial" font-size="11" transform="rotate(-90 18 {(pad_t+H-pad_b)/2})">Bank account balance (dollars)</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q10_value_table() -> str:
    return table_svg("", ["x", "y"], [["1", "13"], ["2", "21"], ["3", "a"]], [80, 80])


def math1_q12_triangle() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="320" viewBox="0 0 420 320">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="80,260 80,60 340,260" fill="none" stroke="#111" stroke-width="2.5"/>
  <rect x="80" y="240" width="20" height="20" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="55" y="165" font-family="Arial" font-size="16">39</text>
  <text x="190" y="285" font-family="Arial" font-size="16">40</text>
  <text x="300" y="235" font-family="Arial" font-size="16">x°</text>
  <text x="210" y="305" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math1_q13_triangle() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="320" viewBox="0 0 420 320">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="80,260 80,60 340,260" fill="none" stroke="#111" stroke-width="2.5"/>
  <rect x="80" y="240" width="20" height="20" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="55" y="165" font-family="Arial" font-size="16">22</text>
  <text x="190" y="285" font-family="Arial" font-size="16">39</text>
  <text x="210" y="155" font-family="Arial" font-size="16" font-style="italic">c</text>
  <text x="300" y="235" font-family="Arial" font-size="16">x°</text>
  <text x="210" y="305" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math1_q15_table() -> str:
    return table_svg("", ["x", "g(x)"], [["1", "46"], ["2", "43"], ["3", "40"], ["4", "37"]], [80, 80])


def math2_q11_dot_plots() -> str:
    W, H = 520, 220
    pad = 40
    plot_w = 180
    # Data set A: 9:1, 10:2, 11:4, 12:2, 13:1
    # Data set B: 10:1, 11:2, 12:4, 13:2, 14:1
    datasets = [
        ("Data set A", {9: 1, 10: 2, 11: 4, 12: 2, 13: 1}),
        ("Data set B", {10: 1, 11: 2, 12: 4, 13: 2, 14: 1}),
    ]

    def panel(title: str, counts: dict[int, int], x0: int) -> str:
        parts = [
            f'<text x="{x0 + plot_w/2}" y="24" text-anchor="middle" font-family="Arial" font-size="13" font-weight="700">{title}</text>'
        ]
        baseline = H - 50
        for v in range(8, 15):
            x = x0 + (v - 8) / 6 * plot_w
            parts.append(
                f'<line x1="{x}" y1="{baseline}" x2="{x}" y2="{baseline-4}" stroke="#111"/>'
                f'<text x="{x}" y="{baseline+16}" text-anchor="middle" font-family="Arial" font-size="11">{v}</text>'
            )
        parts.append(f'<line x1="{x0}" y1="{baseline}" x2="{x0+plot_w}" y2="{baseline}" stroke="#111"/>')
        for val, cnt in counts.items():
            x = x0 + (val - 8) / 6 * plot_w
            for i in range(cnt):
                cy = baseline - 12 - i * 14
                parts.append(f'<circle cx="{x}" cy="{cy}" r="5" fill="#111"/>')
        parts.append(
            f'<text x="{x0 + plot_w/2}" y="{H-8}" text-anchor="middle" font-family="Arial" font-size="12">Value</text>'
        )
        return "\n".join(parts)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {panel("Data set A", datasets[0][1], pad)}
  {panel("Data set B", datasets[1][1], pad + plot_w + 60)}
</svg>'''


def main() -> None:
    write("eng1-q10-tribal-nations-california.svg", eng1_q10_tribal_nations())
    write("eng1-q13-urban-agriculture-ratings.svg", eng1_q13_urban_agriculture())
    write("eng1-q14-honeybee-cells.svg", eng1_q14_honeybee())
    write("eng2-q11-cougar-density.svg", eng2_q11_cougar())
    write("math1-q08-bank-account-graph.svg", math1_q08_bank_graph())
    write("math1-q10-value-table.svg", math1_q10_value_table())
    write("math1-q12-right-triangle.svg", math1_q12_triangle())
    write("math1-q13-right-triangle.svg", math1_q13_triangle())
    write("math1-q15-linear-function-table.svg", math1_q15_table())
    write("math2-q11-dot-plots.svg", math2_q11_dot_plots())
    print("done all purplebook-test-3 figures")


if __name__ == "__main__":
    main()
