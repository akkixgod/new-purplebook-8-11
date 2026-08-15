#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2025 August INT V1."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-august-int-v1/figures")
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def table_svg(
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[int] | None = None,
    blank_first_header: bool = False,
) -> str:
    n = len(headers)
    widths = col_widths or ([180] + [140] * (n - 1))
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
        label = "" if (blank_first_header and i == 0 and not h) else esc(h)
        header_cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{row_h}" fill="#f3f4f6" stroke="#111" stroke-width="1"/>'
            f'<text x="{x + widths[i]/2}" y="{y0 + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="700">{label}</text>'
        )
        x += widths[i]

    for r, row in enumerate(rows):
        y = y0 + row_h * (r + 1)
        x = x0
        for i, cell in enumerate(row):
            body_cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" fill="#fff" stroke="#111" stroke-width="1"/>'
                f'<text x="{x + widths[i]/2}" y="{y + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="13">{esc(cell)}</text>'
            )
            x += widths[i]

    title_el = (
        f'<text x="{width/2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="15" font-weight="700">{esc(title)}</text>'
        if title
        else ""
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {title_el}
  {"".join(header_cells)}
  {"".join(body_cells)}
</svg>'''


def bank_line_graph() -> str:
    W, H = 640, 420
    pad_l, pad_r, pad_t, pad_b = 80, 40, 40, 90
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    x_max, y_max = 10, 80

    def sx(x: float) -> float:
        return pad_l + (x / x_max) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((y_max - y) / y_max) * plot_h

    grid = []
    for v in range(0, 81, 5):
        major = v % 10 == 0
        grid.append(
            f'<line x1="{pad_l}" y1="{sy(v)}" x2="{pad_l+plot_w}" y2="{sy(v)}" stroke="{"#d1d5db" if major else "#eee"}"/>'
        )
        if major and v > 0:
            grid.append(
                f'<text x="{pad_l-10}" y="{sy(v)+4}" text-anchor="end" font-family="Arial" font-size="12">{v}</text>'
            )
    for v in range(0, 11):
        major = v % 2 == 0
        grid.append(
            f'<line x1="{sx(v)}" y1="{pad_t}" x2="{sx(v)}" y2="{pad_t+plot_h}" stroke="{"#d1d5db" if major else "#eee"}"/>'
        )
        if major:
            grid.append(
                f'<text x="{sx(v)}" y="{pad_t+plot_h+22}" text-anchor="middle" font-family="Arial" font-size="12">{v}</text>'
            )

    line = f'<line x1="{sx(0)}" y1="{sy(15)}" x2="{sx(10)}" y2="{sy(55)}" stroke="#111" stroke-width="2.5"/>'
    axes = (
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    xlab = f'<text x="{pad_l+plot_w/2}" y="{H-18}" text-anchor="middle" font-family="Arial" font-size="13">Time since initial deposit (months)</text>'
    ylab = f'<text x="22" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="Arial" font-size="13" transform="rotate(-90 22 {pad_t+plot_h/2})">Bank account balance (dollars)</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  {axes}
  {line}
  {xlab}
  {ylab}
</svg>'''


def dot_plots() -> str:
    W, H = 720, 320
    # Data Set A: values 4-10 counts 1,2,4,5,4,2,1
    # Data Set B: values 4-10 counts 2,3,4,3,4,3,2
    a = [1, 2, 4, 5, 4, 2, 1]
    b = [2, 3, 4, 3, 4, 3, 2]
    values = list(range(4, 11))
    left_x0, right_x0 = 80, 400
    base_y = 250
    gap = 36
    r = 8

    def plot(x0: int, counts: list[int], title: str) -> str:
        parts = [
            f'<text x="{x0 + 3*gap}" y="36" text-anchor="middle" font-family="Georgia, serif" font-size="15" font-weight="700">{title}</text>'
        ]
        for i, (val, cnt) in enumerate(zip(values, counts)):
            x = x0 + i * gap
            parts.append(
                f'<text x="{x}" y="{base_y+24}" text-anchor="middle" font-family="Arial" font-size="12">{val}</text>'
            )
            for k in range(cnt):
                cy = base_y - 14 - k * (2 * r + 2)
                parts.append(f'<circle cx="{x}" cy="{cy}" r="{r}" fill="#111"/>')
        parts.append(
            f'<line x1="{x0-20}" y1="{base_y}" x2="{x0+6*gap+20}" y2="{base_y}" stroke="#111" stroke-width="1.5"/>'
        )
        return "".join(parts)

    xlab = f'<text x="{W/2}" y="{H-16}" text-anchor="middle" font-family="Arial" font-size="13">Value</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {plot(left_x0, a, "Data Set A")}
  {plot(right_x0, b, "Data Set B")}
  {xlab}
</svg>'''


def scatter_lobf() -> str:
    W, H = 560, 480
    pad_l, pad_r, pad_t, pad_b = 60, 40, 30, 50
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    x_max, y_max = 10, 110

    def sx(x: float) -> float:
        return pad_l + (x / x_max) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((y_max - y) / y_max) * plot_h

    grid = []
    for v in range(0, 111, 10):
        grid.append(
            f'<line x1="{pad_l}" y1="{sy(v)}" x2="{pad_l+plot_w}" y2="{sy(v)}" stroke="#e5e7eb"/>'
        )
        if v > 0:
            grid.append(
                f'<text x="{pad_l-8}" y="{sy(v)+4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>'
            )
    for v in range(0, 11):
        grid.append(
            f'<line x1="{sx(v)}" y1="{pad_t}" x2="{sx(v)}" y2="{pad_t+plot_h}" stroke="#e5e7eb"/>'
        )
        if v % 2 == 0 and v > 0:
            grid.append(
                f'<text x="{sx(v)}" y="{pad_t+plot_h+18}" text-anchor="middle" font-family="Arial" font-size="11">{v}</text>'
            )

    # line (0,82)-(10,97)
    line = f'<line x1="{sx(0)}" y1="{sy(82)}" x2="{sx(10)}" y2="{sy(97)}" stroke="#111" stroke-width="2"/>'
    pts = [
        (3.5, 90),
        (5.5, 87),
        (6.0, 94),
        (6.5, 95),
        (6.8, 89),
        (7.3, 90),
        (8.4, 98),
        (9.3, 93),
        (9.8, 100),
    ]
    dots = "".join(
        f'<circle cx="{sx(x)}" cy="{sy(y)}" r="5" fill="#111"/>' for x, y in pts
    )
    axes = (
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    xlab = f'<text x="{pad_l+plot_w/2}" y="{H-12}" text-anchor="middle" font-family="Arial, serif" font-size="14" font-style="italic">x</text>'
    ylab = f'<text x="18" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="Arial, serif" font-size="14" font-style="italic" transform="rotate(-90 18 {pad_t+plot_h/2})">y</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  {axes}
  {line}
  {dots}
  {xlab}
  {ylab}
</svg>'''


def inequality_graph() -> str:
    W, H = 480, 400
    pad = 50
    # x from -6 to 10, y from -6 to 8
    xmin, xmax, ymin, ymax = -6, 10, -6, 8

    def sx(x: float) -> float:
        return pad + ((x - xmin) / (xmax - xmin)) * (W - 2 * pad)

    def sy(y: float) -> float:
        return pad + ((ymax - y) / (ymax - ymin)) * (H - 2 * pad)

    grid = []
    for x in range(xmin, xmax + 1):
        grid.append(
            f'<line x1="{sx(x)}" y1="{pad}" x2="{sx(x)}" y2="{H-pad}" stroke="#eee"/>'
        )
        if x % 2 == 0:
            grid.append(
                f'<text x="{sx(x)}" y="{H-pad+16}" text-anchor="middle" font-family="Arial" font-size="11">{x}</text>'
            )
    for y in range(ymin, ymax + 1):
        grid.append(
            f'<line x1="{pad}" y1="{sy(y)}" x2="{W-pad}" y2="{sy(y)}" stroke="#eee"/>'
        )
        if y % 2 == 0 and y != 0:
            grid.append(
                f'<text x="{pad-8}" y="{sy(y)+4}" text-anchor="end" font-family="Arial" font-size="11">{y}</text>'
            )

    # shade y <= -3x+7 and y <= x-5
    # polygon of feasible region within view
    # intersection at (3,-2)
    # line1: y=-3x+7 from left to intersection then continue
    # Find clip points
    # For shading: sample polygon
    verts = []
    # bottom-left corner of view that satisfies both
    # At x=-6: y1=25 (above view), y2=-11 (below)
    # At left edge, binding is y<=x-5 → at x=-6, y<=-11 → region empty at left until...
    # Actually for x small, x-5 is very low. Region starts when -3x+7 and x-5 allow y >= ymin.
    # Intersection (3,-2). Region is below both lines.
    # Vertices of clipped region:
    # 1) where y=x-5 meets bottom y=-6: x=-1
    # 2) where y=x-5 meets right/bottom...
    # 3) where y=-3x+7 meets bottom y=-6: -3x+7=-6 → -3x=-13 → x=13/3≈4.333
    # 4) where y=-3x+7 meets right x=10: y=-23 (below)
    # Better polygon:
    # - point where x-5 hits left of plot above ymin: at y=-6, x=-1 → (-1,-6)
    # - intersection (3,-2)
    # - where -3x+7 hits y=-6: (13/3, -6)
    # - then along bottom to (-1,-6)? Between x=-1 and 13/3 bottom is in region if below both.
    # At x=0: need y<=7 and y<=-5 → y<=-5, so bottom y=-6 is in.
    # At x=5: y<=-8 and y<=0 → y<=-8, bottom -6 NOT in. So bottom only until intersection with -3x+7.

    pts = [(-1, -6), (3, -2), (13 / 3, -6)]
    poly = " ".join(f"{sx(x)},{sy(y)}" for x, y in pts)
    shade = f'<polygon points="{poly}" fill="#cccccc" fill-opacity="0.45" stroke="none"/>'

    # lines across plot
    # y=-3x+7: at x=-6 y=25→clip top; at top y=8: -3x+7=8 → -3x=1 → x=-1/3
    # at bottom y=-6: x=13/3
    line1 = f'<line x1="{sx(-1/3)}" y1="{sy(8)}" x2="{sx(13/3)}" y2="{sy(-6)}" stroke="#111" stroke-width="2"/>'
    # y=x-5: at y=8 x=13→clip right; at y=-6 x=-1; at x=10 y=5
    line2 = f'<line x1="{sx(-1)}" y1="{sy(-6)}" x2="{sx(10)}" y2="{sy(5)}" stroke="#111" stroke-width="2"/>'
    open_dot = f'<circle cx="{sx(3)}" cy="{sy(-2)}" r="5" fill="#fff" stroke="#111" stroke-width="2"/>'

    axes = (
        f'<line x1="{pad}" y1="{sy(0)}" x2="{W-pad}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{sx(0)}" y1="{pad}" x2="{sx(0)}" y2="{H-pad}" stroke="#111" stroke-width="1.5"/>'
    )
    xlab = f'<text x="{W-pad+8}" y="{sy(0)-6}" font-family="Arial" font-size="13" font-style="italic">x</text>'
    ylab = f'<text x="{sx(0)+8}" y="{pad+4}" font-family="Arial" font-size="13" font-style="italic">y</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  {shade}
  {axes}
  {line1}
  {line2}
  {open_dot}
  {xlab}
  {ylab}
</svg>'''


def puppy_scatter() -> str:
    W, H = 360, 280
    pad_l, pad_r, pad_t, pad_b = 50, 30, 20, 40
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    x_max, y_max = 10, 60

    def sx(x: float) -> float:
        return pad_l + (x / x_max) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((y_max - y) / y_max) * plot_h

    grid = []
    for v in range(0, 61, 10):
        grid.append(
            f'<line x1="{pad_l}" y1="{sy(v)}" x2="{pad_l+plot_w}" y2="{sy(v)}" stroke="#e5e7eb"/>'
        )
        if v > 0:
            grid.append(
                f'<text x="{pad_l-8}" y="{sy(v)+4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>'
            )
    for v in range(0, 11):
        grid.append(
            f'<line x1="{sx(v)}" y1="{pad_t}" x2="{sx(v)}" y2="{pad_t+plot_h}" stroke="#e5e7eb"/>'
        )
        if v % 2 == 0:
            grid.append(
                f'<text x="{sx(v)}" y="{pad_t+plot_h+16}" text-anchor="middle" font-family="Arial" font-size="11">{v}</text>'
            )
    pts = [(2, 12), (3, 22), (4, 28), (5, 41), (6, 46)]
    dots = "".join(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="4" fill="#111"/>' for x, y in pts)
    axes = (
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    xlab = f'<text x="{pad_l+plot_w/2}" y="{H-8}" text-anchor="middle" font-family="Arial" font-size="13" font-style="italic">x</text>'
    ylab = f'<text x="14" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="Arial" font-size="13" font-style="italic" transform="rotate(-90 14 {pad_t+plot_h/2})">y</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  {axes}
  {dots}
  {xlab}
  {ylab}
</svg>'''


def exponential_graph() -> str:
    W, H = 400, 340
    pad_l, pad_r, pad_t, pad_b = 50, 30, 20, 40
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax, ymin, ymax = -4, 4, -6, 10

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    grid = []
    for x in range(xmin, xmax + 1):
        grid.append(
            f'<line x1="{sx(x)}" y1="{pad_t}" x2="{sx(x)}" y2="{pad_t+plot_h}" stroke="#eee"/>'
        )
        if x % 2 == 0:
            grid.append(
                f'<text x="{sx(x)}" y="{pad_t+plot_h+16}" text-anchor="middle" font-family="Arial" font-size="11">{x}</text>'
            )
    for y in range(ymin, ymax + 1, 2):
        grid.append(
            f'<line x1="{pad_l}" y1="{sy(y)}" x2="{pad_l+plot_w}" y2="{sy(y)}" stroke="#eee"/>'
        )
        if y != 0:
            grid.append(
                f'<text x="{pad_l-8}" y="{sy(y)+4}" text-anchor="end" font-family="Arial" font-size="11">{y}</text>'
            )

    # y = 9^x - 2
    path_pts = []
    for i in range(0, 201):
        x = xmin + (xmax - xmin) * i / 200
        y = (9**x) - 2
        if y > ymax + 1:
            continue
        if y < ymin - 1:
            continue
        path_pts.append(f"{sx(x):.2f},{sy(y):.2f}")
    curve = f'<polyline points="{" ".join(path_pts)}" fill="none" stroke="#111" stroke-width="2.5"/>'
    asymptote = f'<line x1="{pad_l}" y1="{sy(-2)}" x2="{pad_l+plot_w}" y2="{sy(-2)}" stroke="#111" stroke-width="1.5" stroke-dasharray="6 4"/>'
    dots = (
        f'<circle cx="{sx(0)}" cy="{sy(-1)}" r="4.5" fill="#111"/>'
        f'<circle cx="{sx(1)}" cy="{sy(7)}" r="4.5" fill="#111"/>'
    )
    axes = (
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l+plot_w}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  {axes}
  {asymptote}
  {curve}
  {dots}
</svg>'''


def main() -> None:
    write(
        "eng1-q10-table.svg",
        table_svg(
            "Cumulative Counts of Fish in Three Taiwanese Tide Pools, 1999–2018",
            ["Species", "Station 1", "Station 2", "Station 3"],
            [
                ["barred flagtail", "249", "64", "16"],
                ["streaky rockskipper", "125", "139", "610"],
                ["blackspotted rockskipper", "83", "74", "31"],
                ["Cocos frillgoby", "50", "64", "90"],
            ],
            col_widths=[200, 100, 100, 100],
        ),
    )
    write(
        "eng1-q11-table.svg",
        table_svg(
            "Numbers of the 23 Non-native Tree Species Reported and the Insect and Fungus Threats to Them",
            ["Country", "Trees", "Fungi", "Insects"],
            [
                ["Austria", "13", "51", "50"],
                ["Belgium", "4", "13", "11"],
                ["Bulgaria", "9", "14", "16"],
            ],
            col_widths=[120, 90, 90, 90],
        ),
    )
    write("m1-q08.svg", bank_line_graph())
    write("m1-q18.svg", dot_plots())
    write("m1-q19.svg", scatter_lobf())
    write("math2-q07-linear-inequalities.svg", inequality_graph())
    write(
        "math2-q08-xy-table.svg",
        table_svg(
            "",
            ["x", "y"],
            [["0", "n"], ["5", "n + 24"], ["10", "n + 48"]],
            col_widths=[80, 100],
        ),
    )
    write("math2-q12-puppy-scatter.svg", puppy_scatter())
    write("math2-q16-exponential-graph.svg", exponential_graph())
    write(
        "math2-q20-age-group-table.svg",
        table_svg(
            "",
            ["", "0–9 years", "10–19 years", "20+ years", "Total"],
            [
                ["Group A", "15", "11", "4", "30"],
                ["Group B", "4", "5", "21", "30"],
                ["Group C", "11", "14", "5", "30"],
                ["Total", "30", "30", "30", "90"],
            ],
            col_widths=[90, 100, 110, 100, 70],
            blank_first_header=True,
        ),
    )
    write(
        "eng2-q10-table.svg",
        table_svg(
            "Home Video Game Systems of the 1970s and 1980s",
            [
                "System",
                "Manufacturer",
                "System type",
                "Approximate number of units sold worldwide",
            ],
            [
                ["ColecoVision", "Coleco", "console", "2,000,000"],
                ["Intellivision", "Mattel", "console", "3,000,000"],
                ["MSX", "ASCII Corp.", "computer", "4,000,000"],
                ["Game & Watch", "Nintendo", "handheld", "18,600,000"],
            ],
            col_widths=[130, 120, 110, 220],
        ),
    )
    write(
        "eng2-q12-table.svg",
        table_svg(
            "Observed Traits in a Population of Broadleaf Arrowhead, by Flowering Date",
            ["Trait", "Day 5", "Day 10", "Day 15", "Day 20"],
            [
                [
                    "Total number of open male and female flowers per growth unit",
                    "25",
                    "65",
                    "110",
                    "45",
                ],
                [
                    "Estimated reproductive success rate of male flowers",
                    "0.29",
                    "0.29",
                    "0.29",
                    "0.29",
                ],
                ["Proportion of male flowers", "0.45", "0.50", "0.48", "0.13"],
            ],
            col_widths=[360, 70, 70, 70, 70],
        ),
    )


if __name__ == "__main__":
    main()
