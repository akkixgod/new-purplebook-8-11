#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures (no watermarks) for 2026 March Int-A."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2026-march-int-a/figures")
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
        label = "" if (blank_first_header and i == 0 and not h) else h
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
                f'<text x="{x + widths[i]/2}" y="{y + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="13">{cell}</text>'
            )
            x += widths[i]

    title_el = (
        f'<text x="{width/2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="15" font-weight="700">{title}</text>'
        if title
        else ""
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {title_el}
  {"".join(header_cells)}
  {"".join(body_cells)}
</svg>'''


def fish_line_graph() -> str:
    W, H = 640, 460
    pad_l, pad_r, pad_t, pad_b = 70, 40, 70, 90
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    y_max = 65

    def sx(i: float) -> float:
        return pad_l + (i / 3) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((y_max - y) / y_max) * plot_h

    months = ["January 2001", "April 2001", "July 2001", "October 2001"]
    blenny = [62, 2, 3, 1]
    flagtail = [14, 9, 7, 16]
    rock = [1, 1, 5, 4]

    grid = []
    for v in range(0, 66, 5):
        grid.append(
            f'<line x1="{pad_l}" y1="{sy(v)}" x2="{pad_l+plot_w}" y2="{sy(v)}" stroke="#e5e7eb"/>'
        )
        grid.append(
            f'<text x="{pad_l-8}" y="{sy(v)+4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>'
        )

    def series(vals: list[float], dash: str, marker: str) -> str:
        pts = " ".join(f"{sx(i)},{sy(v)}" for i, v in enumerate(vals))
        line = f'<polyline points="{pts}" fill="none" stroke="#111" stroke-width="2" stroke-dasharray="{dash}"/>'
        marks = []
        for i, v in enumerate(vals):
            x, y = sx(i), sy(v)
            if marker == "tri":
                marks.append(
                    f'<polygon points="{x},{y-6} {x-6},{y+5} {x+6},{y+5}" fill="#111"/>'
                )
            elif marker == "sq":
                marks.append(
                    f'<rect x="{x-5}" y="{y-5}" width="10" height="10" fill="#fff" stroke="#111" stroke-width="1.5"/>'
                )
            else:
                marks.append(
                    f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="#111" stroke-width="1.5"/>'
                )
        return line + "".join(marks)

    xlabels = "".join(
        f'<text x="{sx(i)}" y="{pad_t+plot_h+28}" text-anchor="middle" font-family="Arial" font-size="11" transform="rotate(-25 {sx(i)} {pad_t+plot_h+28})">{m}</text>'
        for i, m in enumerate(months)
    )
    legend = (
        f'<polygon points="70,440 64,451 76,451" fill="#111"/>'
        f'<line x1="82" y1="445" x2="110" y2="445" stroke="#111" stroke-width="2"/>'
        f'<text x="116" y="449" font-family="Arial" font-size="12">combtooth blenny</text>'
        f'<rect x="270" y="439" width="10" height="10" fill="#fff" stroke="#111"/>'
        f'<line x1="286" y1="444" x2="314" y2="444" stroke="#111" stroke-width="2" stroke-dasharray="6 4"/>'
        f'<text x="320" y="449" font-family="Arial" font-size="12">barred flagtail</text>'
        f'<circle cx="470" cy="444" r="5" fill="#fff" stroke="#111"/>'
        f'<line x1="482" y1="444" x2="510" y2="444" stroke="#111" stroke-width="2" stroke-dasharray="2 3"/>'
        f'<text x="516" y="449" font-family="Arial" font-size="12">striated rockskipper</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <text x="{W/2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">Fish Population in a Taiwanese Tide Pool, January 2001 to October 2001</text>
  {"".join(grid)}
  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>
  {series(blenny, "0", "tri")}
  {series(flagtail, "6 4", "sq")}
  {series(rock, "2 3", "circ")}
  {xlabels}
  <text x="{pad_l+plot_w/2}" y="{H-8}" text-anchor="middle" font-family="Arial" font-size="13">Month</text>
  <text x="18" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-90 18 {pad_t+plot_h/2})">Number of individual fish observed</text>
  {legend}
</svg>'''


def mobility_bars() -> str:
    W, H = 700, 460
    pad_l, pad_r, pad_t, pad_b = 55, 30, 70, 100
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    cats = ["US 2", "US 3", "US 4", "CI 2", "CI 3", "CI 4"]
    # measured, density, preferences
    data = [
        [0.76, 0.68, 0.47],
        [0.12, 0.20, 0.18],
        [0.05, 0.09, 0.10],
        [0.79, 0.85, 0.42],
        [0.12, 0.13, 0.21],
        [0.02, 0.04, 0.11],
    ]
    colors = ["#4b5563", "#d1d5db", "#111827"]
    group_w = plot_w / len(cats)
    bars = []
    labels = []
    for i, (name, vals) in enumerate(zip(cats, data)):
        gx = pad_l + i * group_w + group_w * 0.18
        bw = group_w * 0.18
        for j, v in enumerate(vals):
            h = v * plot_h
            x = gx + j * (bw + 3)
            y = pad_t + plot_h - h
            bars.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" fill="{colors[j]}"/>')
        labels.append(
            f'<text x="{pad_l + i * group_w + group_w/2}" y="{pad_t+plot_h+22}" text-anchor="middle" font-family="Arial" font-size="12">{name}</text>'
        )
    y_grid = "".join(
        f'<line x1="{pad_l}" y1="{pad_t + plot_h - v*plot_h}" x2="{pad_l+plot_w}" y2="{pad_t + plot_h - v*plot_h}" stroke="#e5e7eb"/>'
        f'<text x="{pad_l-8}" y="{pad_t + plot_h - v*plot_h + 4}" text-anchor="end" font-family="Arial" font-size="11">{v:g}</text>'
        for v in [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    )
    legend = (
        f'<rect x="{pad_l}" y="{H-28}" width="12" height="12" fill="{colors[0]}"/>'
        f'<text x="{pad_l+18}" y="{H-18}" font-family="Arial" font-size="12">measured</text>'
        f'<rect x="{pad_l+110}" y="{H-28}" width="12" height="12" fill="{colors[1]}" stroke="#999"/>'
        f'<text x="{pad_l+128}" y="{H-18}" font-family="Arial" font-size="12">model: emphasis density</text>'
        f'<rect x="{pad_l+320}" y="{H-28}" width="12" height="12" fill="{colors[2]}"/>'
        f'<text x="{pad_l+338}" y="{H-18}" font-family="Arial" font-size="12">model: emphasis preferences</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <text x="{W/2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="700">Proportion of the Three Most Commonly Exhibited Mobility Patterns,</text>
  <text x="{W/2}" y="48" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="700">in the US and Côte d'Ivoire</text>
  {y_grid}
  {"".join(bars)}
  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111"/>
  <line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111"/>
  {"".join(labels)}
  <text x="{pad_l+plot_w/2}" y="{H-48}" text-anchor="middle" font-family="Arial" font-size="12">Mobility pattern by country</text>
  <text x="16" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-90 16 {pad_t+plot_h/2})">Proportion</text>
  {legend}
</svg>'''


def triangle_abc() -> str:
    # Right angle at B (bottom-right); A top; C bottom-left; AB=26; AC=49
    W, H = 420, 360
    A, B, C = (300, 70), (300, 280), (80, 280)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="none" stroke="#111" stroke-width="2"/>
  <rect x="{B[0]-14}" y="{B[1]-14}" width="14" height="14" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="{A[0]+10}" y="{A[1]+6}" font-family="Arial" font-size="16" font-weight="700">A</text>
  <text x="{B[0]+10}" y="{B[1]+22}" font-family="Arial" font-size="16" font-weight="700">B</text>
  <text x="{C[0]-18}" y="{C[1]+22}" font-family="Arial" font-size="16" font-weight="700">C</text>
  <text x="{(A[0]+B[0])/2 + 12}" y="{(A[1]+B[1])/2 + 6}" font-family="Arial" font-size="15">26</text>
  <text x="{(A[0]+C[0])/2 - 18}" y="{(A[1]+C[1])/2}" font-family="Arial" font-size="15">49</text>
  <text x="{W/2}" y="340" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def exponential_graph() -> str:
    # y = -4*(2**x) + 2 ; x -6..6, y -10..4
    W, H = 520, 440
    pad_l, pad_r, pad_t, pad_b = 50, 30, 30, 50
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = -6.0, 6.0
    ymin, ymax = -10.0, 4.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    grid = []
    for i in range(-6, 7):
        grid.append(f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t+plot_h}" stroke="#e5e7eb"/>')
        grid.append(
            f'<text x="{sx(i)}" y="{pad_t+plot_h+18}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>'
        )
    for j in range(-10, 5, 2):
        grid.append(f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l+plot_w}" y2="{sy(j)}" stroke="#e5e7eb"/>')
        grid.append(
            f'<text x="{pad_l-8}" y="{sy(j)+4}" text-anchor="end" font-family="Arial" font-size="11">{j}</text>'
        )

    pts = []
    x = -6.0
    while x <= 1.2:
        y = -4 * (2**x) + 2
        if ymin <= y <= ymax:
            pts.append(f"{sx(x):.2f},{sy(y):.2f}")
        x += 0.05
    path = "M " + " L ".join(pts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l+plot_w}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>
  <path d="{path}" fill="none" stroke="#111" stroke-width="2.5"/>
  <text x="{sx(0)+8}" y="{pad_t+14}" font-family="Arial" font-size="14" font-style="italic">y</text>
  <text x="{pad_l+plot_w-10}" y="{sy(0)-8}" font-family="Arial" font-size="14" font-style="italic">x</text>
  <text x="{sx(0)+6}" y="{sy(0)+16}" font-family="Arial" font-size="12">O</text>
</svg>'''


def scatter_lobf() -> str:
    W, H = 520, 420
    pad_l, pad_r, pad_t, pad_b = 55, 30, 30, 55
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmax, ymax = 45.0, 60.0

    def sx(x: float) -> float:
        return pad_l + (x / xmax) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / ymax) * plot_h

    points = [
        (10, 40), (13, 42), (15, 40), (16, 35), (17, 37), (22, 32),
        (26, 30), (30, 30), (32, 24), (35, 25), (38, 30), (41, 21),
    ]
    grid = []
    for i in range(0, 46, 5):
        grid.append(f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t+plot_h}" stroke="#e5e7eb"/>')
    for j in range(0, 61, 5):
        grid.append(f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l+plot_w}" y2="{sy(j)}" stroke="#e5e7eb"/>')
    labels = "".join(
        f'<text x="{sx(i)}" y="{pad_t+plot_h+20}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>'
        for i in (0, 15, 30, 45)
    ) + "".join(
        f'<text x="{pad_l-8}" y="{sy(j)+4}" text-anchor="end" font-family="Arial" font-size="11">{j}</text>'
        for j in (0, 15, 30, 45, 60)
    )
    dots = "".join(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="4.5" fill="#111"/>' for x, y in points)
    # LOBF approx through (15,38) and (30,28); intercept ~48
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>
  <line x1="{sx(5)}" y1="{sy(48)}" x2="{sx(45)}" y2="{sy(18)}" stroke="#111" stroke-width="2"/>
  {dots}
  {labels}
  <text x="{pad_l+plot_w/2}" y="{H-12}" text-anchor="middle" font-family="Arial" font-size="14" font-style="italic">x</text>
  <text x="16" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="Arial" font-size="14" font-style="italic" transform="rotate(-90 16 {pad_t+plot_h/2})">y</text>
</svg>'''


def q_tables_choices() -> str:
    """Four small tables for math2 q3 choices."""
    opts = [
        ("A", ["-24", "0", "24"]),
        ("B", ["1/6", "2", "24"]),
        ("C", ["1/6", "12", "24"]),
        ("D", ["6", "12", "24"]),
    ]
    panels = []
    for idx, (lab, vals) in enumerate(opts):
        ox = 20 + idx * 240
        cells = []
        headers = ["x", "-1", "0", "1"]
        row2 = ["q(x)"] + vals
        for r, row in enumerate([headers, row2]):
            for c, val in enumerate(row):
                x = ox + c * 50
                y = 40 + r * 36
                fill = "#f3f4f6" if r == 0 or c == 0 else "#fff"
                cells.append(
                    f'<rect x="{x}" y="{y}" width="50" height="36" fill="{fill}" stroke="#111"/>'
                    f'<text x="{x+25}" y="{y+24}" text-anchor="middle" font-family="Arial" font-size="13">{val}</text>'
                )
        panels.append(
            f'<text x="{ox}" y="28" font-family="Arial" font-size="16" font-weight="700">{lab})</text>'
            + "".join(cells)
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="140" viewBox="0 0 1000 140">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(panels)}
</svg>'''


def parallel_lines() -> str:
    # m top, n bottom; transversals AE and CD cross at B
    W, H = 480, 360
    # m: y=90, n: y=260
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <line x1="40" y1="90" x2="420" y2="90" stroke="#111" stroke-width="2"/>
  <line x1="40" y1="260" x2="420" y2="260" stroke="#111" stroke-width="2"/>
  <text x="430" y="94" font-family="Arial" font-size="16" font-style="italic">m</text>
  <text x="430" y="264" font-family="Arial" font-size="16" font-style="italic">n</text>
  <!-- A left on n, C right on n, D left on m, E right on m, B intersection -->
  <line x1="100" y1="260" x2="360" y2="90" stroke="#111" stroke-width="2"/>
  <line x1="360" y1="260" x2="100" y2="90" stroke="#111" stroke-width="2"/>
  <text x="88" y="282" font-family="Arial" font-size="15" font-weight="700">A</text>
  <text x="360" y="282" font-family="Arial" font-size="15" font-weight="700">C</text>
  <text x="88" y="82" font-family="Arial" font-size="15" font-weight="700">D</text>
  <text x="360" y="82" font-family="Arial" font-size="15" font-weight="700">E</text>
  <text x="222" y="182" font-family="Arial" font-size="15" font-weight="700">B</text>
  <text x="{W/2}" y="340" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def main() -> None:
    write(
        "eng1-q10-bears.svg",
        table_svg(
            "Brown Bears in Katmai National Park, Alaska",
            [
                "Bear identification number",
                "Sex",
                "Age (years)",
                "Approximate weight (pounds)",
            ],
            [
                ["173", "female", "10", "400"],
                ["122", "male", "3", "200"],
                ["117", "female", "6", "325"],
                ["103", "male", "4", "275"],
            ],
            [200, 100, 120, 220],
        ),
    )
    write("eng1-q12-fish.svg", fish_line_graph())
    write("eng2-q12-mobility.svg", mobility_bars())
    write(
        "math1-q02-entrees.svg",
        table_svg(
            "",
            ["Type of entree", "Number of people"],
            [
                ["Beef", "17"],
                ["Chicken", "20"],
                ["Fish", "6"],
                ["Vegetarian", "7"],
                ["Total", "50"],
            ],
            [200, 180],
        ),
    )
    write("math1-q12-triangle.svg", triangle_abc())
    write(
        "math1-q13-tx.svg",
        table_svg(
            "",
            ["x", "t(x)"],
            [["29", "15"], ["32", "33/2"], ["51", "26"]],
            [120, 120],
        ),
    )
    write(
        "math1-q19-employees.svg",
        table_svg(
            "",
            ["Number of employees", "Number of stores"],
            [
                ["1 to 6", "2"],
                ["7 to 12", "3"],
                ["13 to 18", "1"],
                ["19 to 24", "6"],
                ["25 to 30", "1"],
            ],
            [200, 180],
        ),
    )
    write("math1-q21-exponential.svg", exponential_graph())
    write("math2-q02-scatter.svg", scatter_lobf())
    write("math2-q03-choices.svg", q_tables_choices())
    write(
        "math2-q09-cars.svg",
        table_svg(
            "",
            ["Number of cars", "Maximum number of passengers and crew"],
            [["3", "139"], ["6", "271"], ["10", "447"]],
            [180, 320],
        ),
    )
    write(
        "math2-q13-xy.svg",
        table_svg(
            "",
            ["x", "y"],
            [["-12", "46"], ["a", "16"], ["2", "b"]],
            [120, 120],
        ),
    )
    write("math2-q16-parallels.svg", parallel_lines())
    write(
        "math2-q21-trapezoids.svg",
        table_svg(
            "",
            ["", "Area (square inches)"],
            [["Trapezoid ABCD", "440"], ["Trapezoid EFGH", "11,000"]],
            [200, 200],
            blank_first_header=True,
        ),
    )


if __name__ == "__main__":
    main()
