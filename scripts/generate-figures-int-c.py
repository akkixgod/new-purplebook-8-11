#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures (no watermarks) for 2026 March Int-C."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2026-march-int-c/figures")
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
    widths = col_widths or ([180] + [140] * (n - 1))
    width = sum(widths) + 40
    row_h = 36
    title_h = 56 if title else 16
    height = title_h + 40 + row_h * (1 + len(rows)) + 20
    x0, y0 = 20, title_h
    cells = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{row_h}" fill="#f3f4f6" stroke="#111"/>'
            f'<text x="{x + widths[i]/2}" y="{y0 + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="700">{h}</text>'
        )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + row_h * (r + 1)
        x = x0
        for i, cell in enumerate(row):
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i]/2}" y="{y + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="13">{cell}</text>'
            )
            x += widths[i]
    title_el = (
        f'<text x="{width/2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">{title}</text>'
        if title
        else ""
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {title_el}
  {"".join(cells)}
</svg>'''


def fish_graph() -> str:
    W, H = 640, 460
    pad_l, pad_r, pad_t, pad_b = 70, 40, 70, 90
    plot_w, plot_h = W - pad_l - pad_r, H - pad_t - pad_b
    y_max = 65.0

    def sx(i: float) -> float:
        return pad_l + (i / 3) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((y_max - y) / y_max) * plot_h

    months = ["January 2001", "April 2001", "July 2001", "October 2001"]
    blenny, flagtail, rock = [62, 3, 3, 1], [14, 10, 8, 16], [0, 0, 4, 4]
    grid = []
    for v in range(0, 66, 5):
        grid.append(f'<line x1="{pad_l}" y1="{sy(v)}" x2="{pad_l+plot_w}" y2="{sy(v)}" stroke="#e5e7eb"/>')
        grid.append(f'<text x="{pad_l-8}" y="{sy(v)+4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>')

    def series(vals, dash, marker):
        pts = " ".join(f"{sx(i)},{sy(v)}" for i, v in enumerate(vals))
        line = f'<polyline points="{pts}" fill="none" stroke="#111" stroke-width="2" stroke-dasharray="{dash}"/>'
        marks = []
        for i, v in enumerate(vals):
            x, y = sx(i), sy(v)
            if marker == "tri":
                marks.append(f'<polygon points="{x},{y-6} {x-6},{y+5} {x+6},{y+5}" fill="#111"/>')
            elif marker == "sq":
                marks.append(f'<rect x="{x-5}" y="{y-5}" width="10" height="10" fill="#fff" stroke="#111" stroke-width="1.5"/>')
            else:
                marks.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="#111" stroke-width="1.5"/>')
        return line + "".join(marks)

    xlabels = "".join(
        f'<text x="{sx(i)}" y="{pad_t+plot_h+28}" text-anchor="middle" font-family="Arial" font-size="11" transform="rotate(-25 {sx(i)} {pad_t+plot_h+28})">{m}</text>'
        for i, m in enumerate(months)
    )
    legend = (
        '<polygon points="70,440 64,451 76,451" fill="#111"/>'
        '<line x1="82" y1="445" x2="110" y2="445" stroke="#111" stroke-width="2"/>'
        '<text x="116" y="449" font-family="Arial" font-size="12">combtooth blenny</text>'
        '<rect x="270" y="439" width="10" height="10" fill="#fff" stroke="#111"/>'
        '<line x1="286" y1="444" x2="314" y2="444" stroke="#111" stroke-width="2" stroke-dasharray="6 4"/>'
        '<text x="320" y="449" font-family="Arial" font-size="12">barred flagtail</text>'
        '<circle cx="470" cy="444" r="5" fill="#fff" stroke="#111"/>'
        '<line x1="482" y1="444" x2="510" y2="444" stroke="#111" stroke-width="2" stroke-dasharray="2 3"/>'
        '<text x="516" y="449" font-family="Arial" font-size="12">striated rockskipper</text>'
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
    W, H = 700, 440
    pad_l, pad_r, pad_t, pad_b = 55, 30, 50, 100
    plot_w, plot_h = W - pad_l - pad_r, H - pad_t - pad_b
    cats = ["US 2", "US 3", "US 4", "CI 2", "CI 3", "CI 4"]
    # measured, density, preferences (College Board-style values)
    data = [
        [0.76, 0.68, 0.47],
        [0.12, 0.20, 0.18],
        [0.05, 0.09, 0.10],
        [0.79, 0.85, 0.35],
        [0.12, 0.13, 0.21],
        [0.04, 0.03, 0.11],
    ]
    colors = ["#111827", "#fff", "#9ca3af"]
    group_w = plot_w / len(cats)
    bars, labels = [], []
    for i, (name, vals) in enumerate(zip(cats, data)):
        gx = pad_l + i * group_w + group_w * 0.18
        bw = group_w * 0.18
        for j, v in enumerate(vals):
            h = (v / 0.8) * plot_h
            x = gx + j * (bw + 3)
            y = pad_t + plot_h - h
            stroke = ' stroke="#111"' if colors[j] == "#fff" else ""
            bars.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" fill="{colors[j]}"{stroke}/>')
        labels.append(
            f'<text x="{pad_l + i * group_w + group_w/2}" y="{pad_t+plot_h+22}" text-anchor="middle" font-family="Arial" font-size="12">{name}</text>'
        )
    y_grid = "".join(
        f'<line x1="{pad_l}" y1="{pad_t + plot_h - (v/0.8)*plot_h}" x2="{pad_l+plot_w}" y2="{pad_t + plot_h - (v/0.8)*plot_h}" stroke="#e5e7eb"/>'
        f'<text x="{pad_l-8}" y="{pad_t + plot_h - (v/0.8)*plot_h + 4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>'
        for v in [0, 0.2, 0.4, 0.6, 0.8]
    )
    legend = (
        f'<rect x="{pad_l}" y="{H-28}" width="12" height="12" fill="{colors[0]}"/>'
        f'<text x="{pad_l+18}" y="{H-18}" font-family="Arial" font-size="12">measured</text>'
        f'<rect x="{pad_l+110}" y="{H-28}" width="12" height="12" fill="#fff" stroke="#111"/>'
        f'<text x="{pad_l+128}" y="{H-18}" font-family="Arial" font-size="12">model: emphasis density</text>'
        f'<rect x="{pad_l+320}" y="{H-28}" width="12" height="12" fill="{colors[2]}"/>'
        f'<text x="{pad_l+338}" y="{H-18}" font-family="Arial" font-size="12">model: emphasis preferences</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <text x="{W/2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">Mobility pattern by country</text>
  {y_grid}
  {"".join(bars)}
  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111"/>
  <line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111"/>
  {"".join(labels)}
  <text x="16" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-90 16 {pad_t+plot_h/2})">Proportion</text>
  {legend}
</svg>'''


def choice_tables_m1q2() -> str:
    opts = [
        ("A", [["28", "27"], ["29", "28"], ["30", "29"]]),
        ("B", [["28", "29"], ["29", "30"], ["30", "31"]]),
        ("C", [["32", "31"], ["33", "32"], ["34", "33"]]),
        ("D", [["32", "33"], ["29", "30"], ["30", "31"]]),
    ]
    panels = []
    for idx, (lab, rows) in enumerate(opts):
        ox = 20 + (idx % 2) * 240
        oy = 20 + (idx // 2) * 180
        cells = []
        for r, row in enumerate([["x", "y"]] + rows):
            for c, val in enumerate(row):
                x, y = ox + c * 70, oy + 24 + r * 32
                fill = "#f3f4f6" if r == 0 else "#fff"
                cells.append(
                    f'<rect x="{x}" y="{y}" width="70" height="32" fill="{fill}" stroke="#111"/>'
                    f'<text x="{x+35}" y="{y+22}" text-anchor="middle" font-family="Arial" font-size="14">{val}</text>'
                )
        panels.append(f'<text x="{ox}" y="{oy+16}" font-family="Arial" font-size="16" font-weight="700">{lab})</text>' + "".join(cells))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="380" viewBox="0 0 520 380">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(panels)}
</svg>'''


def similar_triangles() -> str:
    # DEF left (smaller), QRS right (larger) with kf, kd, ke
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="560" height="300" viewBox="0 0 560 300">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="40,220 120,60 200,220" fill="none" stroke="#111" stroke-width="2"/>
  <text x="30" y="240" font-family="Arial" font-size="16" font-weight="700">D</text>
  <text x="118" y="52" font-family="Arial" font-size="16" font-weight="700">E</text>
  <text x="200" y="240" font-family="Arial" font-size="16" font-weight="700">F</text>
  <text x="70" y="130" font-family="Arial" font-size="15" font-style="italic">f</text>
  <text x="165" y="130" font-family="Arial" font-size="15" font-style="italic">d</text>
  <text x="115" y="245" font-family="Arial" font-size="15" font-style="italic">e</text>
  <polygon points="280,240 400,40 520,240" fill="none" stroke="#111" stroke-width="2"/>
  <text x="268" y="260" font-family="Arial" font-size="16" font-weight="700">Q</text>
  <text x="396" y="32" font-family="Arial" font-size="16" font-weight="700">R</text>
  <text x="520" y="260" font-family="Arial" font-size="16" font-weight="700">S</text>
  <text x="320" y="130" font-family="Arial" font-size="15" font-style="italic">kf</text>
  <text x="465" y="130" font-family="Arial" font-size="15" font-style="italic">kd</text>
  <text x="385" y="265" font-family="Arial" font-size="15" font-style="italic">ke</text>
  <text x="280" y="290" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def line_k() -> str:
    W, H = 480, 440
    pad = 50
    plot = 360

    def sx(x):
        return pad + ((x + 11) / 22) * plot

    def sy(y):
        return pad + ((11 - y) / 22) * plot

    grid = []
    for i in range(-10, 11, 2):
        grid.append(f'<line x1="{sx(i)}" y1="{pad}" x2="{sx(i)}" y2="{pad+plot}" stroke="#e5e7eb"/>')
        grid.append(f'<line x1="{pad}" y1="{sy(i)}" x2="{pad+plot}" y2="{sy(i)}" stroke="#e5e7eb"/>')
        grid.append(f'<text x="{sx(i)}" y="{pad+plot+18}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>')
        grid.append(f'<text x="{pad-8}" y="{sy(i)+4}" text-anchor="end" font-family="Arial" font-size="11">{i}</text>')
    # line through (-2,2) and (2,-3): slope -5/4
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <line x1="{sx(0)}" y1="{pad}" x2="{sx(0)}" y2="{pad+plot}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad}" y1="{sy(0)}" x2="{pad+plot}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>
  <line x1="{sx(-6)}" y1="{sy(7)}" x2="{sx(6)}" y2="{sy(-8)}" stroke="#111" stroke-width="2.5"/>
  <circle cx="{sx(-2)}" cy="{sy(2)}" r="4" fill="#111"/>
  <circle cx="{sx(2)}" cy="{sy(-3)}" r="4" fill="#111"/>
  <text x="{sx(4)}" y="{sy(-4)}" font-family="Arial" font-size="14" font-style="italic">k</text>
  <text x="{sx(0)+6}" y="{sy(0)+16}" font-family="Arial" font-size="12">O</text>
  <text x="{pad+plot-10}" y="{sy(0)-8}" font-family="Arial" font-size="14" font-style="italic">x</text>
  <text x="{sx(0)+8}" y="{pad+14}" font-family="Arial" font-size="14" font-style="italic">y</text>
</svg>'''


def exponential_m1q14() -> str:
    # y = -6*(2**x) + 2
    W, H = 520, 440
    pad_l, pad_r, pad_t, pad_b = 50, 30, 30, 50
    plot_w, plot_h = W - pad_l - pad_r, H - pad_t - pad_b
    xmin, xmax, ymin, ymax = -6.0, 6.0, -10.0, 4.0

    def sx(x):
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y):
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    grid = []
    for i in range(-6, 7):
        grid.append(f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t+plot_h}" stroke="#e5e7eb"/>')
        grid.append(f'<text x="{sx(i)}" y="{pad_t+plot_h+18}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>')
    for j in range(-10, 5, 2):
        grid.append(f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l+plot_w}" y2="{sy(j)}" stroke="#e5e7eb"/>')
        grid.append(f'<text x="{pad_l-8}" y="{sy(j)+4}" text-anchor="end" font-family="Arial" font-size="11">{j}</text>')
    pts = []
    x = -6.0
    while x <= 1.3:
        y = -6 * (2**x) + 2
        if ymin <= y <= ymax:
            pts.append(f"{sx(x):.2f},{sy(y):.2f}")
        x += 0.05
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l+plot_w}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>
  <path d="M {" L ".join(pts)}" fill="none" stroke="#111" stroke-width="2.5"/>
  <text x="{sx(0)+6}" y="{sy(0)+16}" font-family="Arial" font-size="12">O</text>
  <text x="{pad_l+plot_w-10}" y="{sy(0)-8}" font-family="Arial" font-size="14" font-style="italic">x</text>
  <text x="{sx(0)+8}" y="{pad_t+14}" font-family="Arial" font-size="14" font-style="italic">y</text>
</svg>'''


def linear_m1q20() -> str:
    # line through (0,4) and (2,0): y = -2x + 4
    W, H = 500, 440
    pad = 50
    plot = 360

    def sx(x):
        return pad + ((x + 6) / 16) * plot

    def sy(y):
        return pad + ((11 - y) / 18) * plot

    grid = []
    for i in range(-6, 11, 2):
        grid.append(f'<line x1="{sx(i)}" y1="{pad}" x2="{sx(i)}" y2="{pad+plot}" stroke="#e5e7eb"/>')
        grid.append(f'<text x="{sx(i)}" y="{pad+plot+18}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>')
    for j in range(-6, 11, 2):
        grid.append(f'<line x1="{pad}" y1="{sy(j)}" x2="{pad+plot}" y2="{sy(j)}" stroke="#e5e7eb"/>')
        grid.append(f'<text x="{pad-8}" y="{sy(j)+4}" text-anchor="end" font-family="Arial" font-size="11">{j}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <line x1="{sx(0)}" y1="{pad}" x2="{sx(0)}" y2="{pad+plot}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad}" y1="{sy(0)}" x2="{pad+plot}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>
  <line x1="{sx(-1)}" y1="{sy(6)}" x2="{sx(5)}" y2="{sy(-6)}" stroke="#111" stroke-width="2.5"/>
  <circle cx="{sx(0)}" cy="{sy(4)}" r="4" fill="#111"/>
  <circle cx="{sx(2)}" cy="{sy(0)}" r="4" fill="#111"/>
  <text x="{sx(0)+6}" y="{sy(0)+16}" font-family="Arial" font-size="12">O</text>
  <text x="{pad+plot-10}" y="{sy(0)-8}" font-family="Arial" font-size="14" font-style="italic">x</text>
  <text x="{sx(0)+8}" y="{pad+14}" font-family="Arial" font-size="14" font-style="italic">y</text>
</svg>'''


def exponential_m2q2() -> str:
    # y = 3^x + 10; asymptote y=10, through (0,11)
    W, H = 520, 420
    pad_l, pad_r, pad_t, pad_b = 50, 30, 30, 50
    plot_w, plot_h = W - pad_l - pad_r, H - pad_t - pad_b
    xmin, xmax, ymin, ymax = -8.0, 8.0, 0.0, 14.0

    def sx(x):
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y):
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    grid = []
    for i in range(-8, 9, 2):
        grid.append(f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t+plot_h}" stroke="#e5e7eb"/>')
        grid.append(f'<text x="{sx(i)}" y="{pad_t+plot_h+18}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>')
    for j in range(0, 15, 2):
        grid.append(f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l+plot_w}" y2="{sy(j)}" stroke="#e5e7eb"/>')
        grid.append(f'<text x="{pad_l-8}" y="{sy(j)+4}" text-anchor="end" font-family="Arial" font-size="11">{j}</text>')
    pts = []
    x = -8.0
    while x <= 1.6:
        y = (3**x) + 10
        if ymin <= y <= ymax:
            pts.append(f"{sx(x):.2f},{sy(y):.2f}")
        x += 0.05
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l+plot_w}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>
  <path d="M {" L ".join(pts)}" fill="none" stroke="#111" stroke-width="2.5"/>
  <text x="{sx(0)+6}" y="{sy(0)-8}" font-family="Arial" font-size="12">O</text>
  <text x="{pad_l+plot_w-10}" y="{sy(0)-8}" font-family="Arial" font-size="14" font-style="italic">x</text>
  <text x="{sx(0)+8}" y="{pad_t+14}" font-family="Arial" font-size="14" font-style="italic">y</text>
</svg>'''


def temp_scatter() -> str:
    W, H = 560, 420
    pad_l, pad_r, pad_t, pad_b = 70, 30, 30, 60
    plot_w, plot_h = W - pad_l - pad_r, H - pad_t - pad_b
    xmax, ymax = 8000.0, 80.0

    def sx(x):
        return pad_l + (x / xmax) * plot_w

    def sy(y):
        return pad_t + ((ymax - y) / ymax) * plot_h

    points = [(500, 54), (1200, 51), (2500, 39), (4800, 25), (6200, 15), (7200, 12)]
    grid = []
    for i in range(0, 8001, 1000):
        grid.append(f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t+plot_h}" stroke="#e5e7eb"/>')
    for j in range(0, 81, 10):
        grid.append(f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l+plot_w}" y2="{sy(j)}" stroke="#e5e7eb"/>')
        grid.append(f'<text x="{pad_l-8}" y="{sy(j)+4}" text-anchor="end" font-family="Arial" font-size="11">{j}</text>')
    labels = "".join(
        f'<text x="{sx(i)}" y="{pad_t+plot_h+20}" text-anchor="middle" font-family="Arial" font-size="11">{i:,}</text>'
        for i in (0, 2000, 4000, 6000, 8000)
    )
    dots = "".join(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="4.5" fill="#111"/>' for x, y in points)
    # LOBF through (0,54) and (4000,30)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>
  <line x1="{sx(0)}" y1="{sy(54)}" x2="{sx(8000)}" y2="{sy(6)}" stroke="#111" stroke-width="2"/>
  {dots}
  {labels}
  <text x="{pad_l+plot_w/2}" y="{H-12}" text-anchor="middle" font-family="Arial" font-size="13">Elevation (feet)</text>
  <text x="18" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="Arial" font-size="13" transform="rotate(-90 18 {pad_t+plot_h/2})">Temperature (°F)</text>
</svg>'''


def line_and_parabola() -> str:
    # y=2 horizontal; parabola vertex (-3,2) opening down
    W, H = 500, 420
    pad = 50
    plot = 340

    def sx(x):
        return pad + ((x + 11) / 16) * plot

    def sy(y):
        return pad + ((7 - y) / 12) * plot

    grid = []
    for i in range(-10, 5, 2):
        grid.append(f'<line x1="{sx(i)}" y1="{pad}" x2="{sx(i)}" y2="{pad+plot}" stroke="#e5e7eb"/>')
        grid.append(f'<text x="{sx(i)}" y="{pad+plot+18}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>')
    for j in range(-4, 7, 2):
        grid.append(f'<line x1="{pad}" y1="{sy(j)}" x2="{pad+plot}" y2="{sy(j)}" stroke="#e5e7eb"/>')
        grid.append(f'<text x="{pad-8}" y="{sy(j)+4}" text-anchor="end" font-family="Arial" font-size="11">{j}</text>')
    pts = []
    x = -8.0
    while x <= 2.0:
        y = 2 - 0.25 * (x + 3) ** 2
        if -5 <= y <= 7:
            pts.append(f"{sx(x):.2f},{sy(y):.2f}")
        x += 0.05
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <line x1="{sx(0)}" y1="{pad}" x2="{sx(0)}" y2="{pad+plot}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad}" y1="{sy(0)}" x2="{pad+plot}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad}" y1="{sy(2)}" x2="{pad+plot}" y2="{sy(2)}" stroke="#111" stroke-width="2"/>
  <path d="M {" L ".join(pts)}" fill="none" stroke="#111" stroke-width="2.5"/>
  <text x="{sx(0)+6}" y="{sy(0)+16}" font-family="Arial" font-size="12">O</text>
</svg>'''


def main() -> None:
    write("eng1-q12-fish.svg", fish_graph())
    write(
        "eng2-q10-strontium.svg",
        table_svg(
            "Strontium Isotope Ratios and Corresponding Numerical Ages in the Global Seawater Curve",
            ["⁸⁷Sr / ⁸⁶Sr", "Age (Ma)"],
            [
                ["0.708980", "6.20"],
                ["0.709000", "5.86"],
                ["0.709020", "5.40"],
                ["0.709040", "4.75"],
                ["0.709060", "3.00"],
            ],
            [200, 160],
        ),
    )
    write("eng2-q11-mobility.svg", mobility_bars())
    write("math1-q02-tables.svg", choice_tables_m1q2())
    write("math1-q11-triangles.svg", similar_triangles())
    write("math1-q13-line-k.svg", line_k())
    write("math1-q14-exponential.svg", exponential_m1q14())
    write("math1-q20-line.svg", linear_m1q20())
    write("math2-q02-exponential.svg", exponential_m2q2())
    write("math2-q06-scatter.svg", temp_scatter())
    write("math2-q07-line-parabola.svg", line_and_parabola())
    write(
        "math2-q15-pitching.svg",
        table_svg(
            "",
            ["Average pitching speed", "Number of pitchers"],
            [
                ["At least 30 mph but less than 35 mph", "12"],
                ["At least 35 mph but less than 40 mph", "7"],
                ["At least 40 mph but less than 45 mph", "4"],
                ["At least 45 mph but less than 50 mph", "1"],
            ],
            [340, 160],
        ),
    )
    write(
        "math2-q21-hx.svg",
        table_svg("", ["x", "h(x)"], [["0", "15"], ["1", "16"], ["2", "18"]], [100, 100]),
    )


if __name__ == "__main__":
    main()
