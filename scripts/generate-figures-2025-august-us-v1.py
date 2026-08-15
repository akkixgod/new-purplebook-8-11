#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2025 August US V1."""

from __future__ import annotations

import math
from pathlib import Path

OUT = Path("public/mocks/2025-august-us-v1/figures")
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


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
    x0, y0 = 20, title_h
    cells = []
    x = x0
    for i, h in enumerate(headers):
        label = "" if (blank_first_header and i == 0 and not h) else esc(h)
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{row_h}" fill="#f3f4f6" stroke="#111" stroke-width="1"/>'
            f'<text x="{x + widths[i]/2}" y="{y0 + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="700">{label}</text>'
        )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + row_h * (r + 1)
        x = x0
        for i, cell in enumerate(row):
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" fill="#fff" stroke="#111" stroke-width="1"/>'
                f'<text x="{x + widths[i]/2}" y="{y + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="12">{esc(cell)}</text>'
            )
            x += widths[i]
    title_el = (
        f'<text x="{width/2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">{esc(title)}</text>'
        if title
        else ""
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {title_el}
  {"".join(cells)}
</svg>'''


def w_curve_graph() -> str:
    W, H = 520, 380
    pad_l, pad_r, pad_t, pad_b = 50, 40, 30, 40
    plot_w, plot_h = W - pad_l - pad_r, H - pad_t - pad_b
    xmin, xmax, ymin, ymax = -10, 10, 0, 12

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    grid = []
    for x in range(xmin, xmax + 1):
        grid.append(f'<line x1="{sx(x)}" y1="{pad_t}" x2="{sx(x)}" y2="{pad_t+plot_h}" stroke="#eee"/>')
        if x % 2 == 0:
            grid.append(f'<text x="{sx(x)}" y="{pad_t+plot_h+16}" text-anchor="middle" font-family="Arial" font-size="11">{x}</text>')
    for y in range(ymin, ymax + 1):
        grid.append(f'<line x1="{pad_l}" y1="{sy(y)}" x2="{pad_l+plot_w}" y2="{sy(y)}" stroke="#eee"/>')
        if y % 2 == 0:
            grid.append(f'<text x="{pad_l-8}" y="{sy(y)+4}" text-anchor="end" font-family="Arial" font-size="11">{y}</text>')

    # Smooth W: mins (-3,4),(3,4), max (0,7)
    pts = []
    for i in range(0, 201):
        x = -6 + 12 * i / 200
        # quartic-ish: a(x^2-9)^2 + 4 with a chosen so f(0)=7 → a*81+4=7 → a=3/81=1/27
        y = (1 / 27) * (x * x - 9) ** 2 + 4
        if ymin <= y <= ymax + 0.5:
            pts.append(f"{sx(x):.2f},{sy(y):.2f}")
    curve = f'<polyline points="{" ".join(pts)}" fill="none" stroke="#111" stroke-width="2.5"/>'
    axes = (
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l+plot_w}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  {axes}
  {curve}
</svg>'''


def right_triangle_abc() -> str:
    # A top, C bottom-left, B bottom-right with right angle at B
    # AB=29 vertical, CA=47 hypotenuse
    W, H = 360, 300
    Ax, Ay = 80, 40
    Bx, By = 80, 240
    Cx, Cy = 280, 240
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="{Ax},{Ay} {Bx},{By} {Cx},{Cy}" fill="none" stroke="#111" stroke-width="2"/>
  <rect x="{Bx}" y="{By-18}" width="18" height="18" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="{Ax-18}" y="{Ay+8}" font-family="Georgia, serif" font-size="16">A</text>
  <text x="{Bx-18}" y="{By+22}" font-family="Georgia, serif" font-size="16">B</text>
  <text x="{Cx+8}" y="{Cy+22}" font-family="Georgia, serif" font-size="16">C</text>
  <text x="{Ax-28}" y="{(Ay+By)/2+5}" font-family="Arial" font-size="14">29</text>
  <text x="{(Ax+Cx)/2+10}" y="{(Ay+Cy)/2}" font-family="Arial" font-size="14">47</text>
  <text x="{W/2}" y="{H-12}" text-anchor="middle" font-family="Arial" font-size="12">Note: Figure not drawn to scale.</text>
</svg>'''


def scatter_lobf() -> str:
    W, H = 400, 360
    pad_l, pad_r, pad_t, pad_b = 45, 30, 25, 40
    plot_w, plot_h = W - pad_l - pad_r, H - pad_t - pad_b
    mx = 6

    def sx(x: float) -> float:
        return pad_l + (x / mx) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((mx - y) / mx) * plot_h

    grid = []
    for v in range(0, 7):
        grid.append(f'<line x1="{sx(v)}" y1="{pad_t}" x2="{sx(v)}" y2="{pad_t+plot_h}" stroke="#e5e7eb"/>')
        grid.append(f'<line x1="{pad_l}" y1="{sy(v)}" x2="{pad_l+plot_w}" y2="{sy(v)}" stroke="#e5e7eb"/>')
        grid.append(f'<text x="{sx(v)}" y="{pad_t+plot_h+16}" text-anchor="middle" font-family="Arial" font-size="11">{v}</text>')
        if v > 0:
            grid.append(f'<text x="{pad_l-8}" y="{sy(v)+4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>')
    line = f'<line x1="{sx(0)}" y1="{sy(0)}" x2="{sx(6)}" y2="{sy(4.2)}" stroke="#111" stroke-width="2"/>'
    pts = [(0, 0), (0.8, 0.5), (1.4, 1.3), (2.0, 2.0), (2.4, 1.2), (3.0, 2.5), (3.5, 2.5), (4.0, 2.6), (4.5, 3.6), (5.0, 2.9), (5.5, 4.1), (5.8, 3.8)]
    dots = "".join(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="4" fill="#111"/>' for x, y in pts)
    axes = (
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  {axes}
  {line}
  {dots}
  <text x="{sx(0)-10}" y="{sy(0)+14}" font-family="Arial" font-size="12">O</text>
  <text x="{pad_l+plot_w+8}" y="{pad_t+plot_h}" font-family="Arial" font-size="13" font-style="italic">x</text>
  <text x="{pad_l+8}" y="{pad_t+12}" font-family="Arial" font-size="13" font-style="italic">y</text>
</svg>'''


def overlapping_triangles() -> str:
    W, H = 420, 280
    # A G F E on base; B above A; D above E; intersect C
    A, G, F, E = (60, 220), (150, 220), (250, 220), (360, 220)
    B, D = (60, 60), (360, 60)
    # BF from B to F, DG from D to G; intersection approx
    C = (200, 130)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <line x1="{A[0]}" y1="{A[1]}" x2="{E[0]}" y2="{E[1]}" stroke="#111" stroke-width="2"/>
  <line x1="{A[0]}" y1="{A[1]}" x2="{B[0]}" y2="{B[1]}" stroke="#111" stroke-width="2"/>
  <line x1="{B[0]}" y1="{B[1]}" x2="{F[0]}" y2="{F[1]}" stroke="#111" stroke-width="2"/>
  <line x1="{E[0]}" y1="{E[1]}" x2="{D[0]}" y2="{D[1]}" stroke="#111" stroke-width="2"/>
  <line x1="{D[0]}" y1="{D[1]}" x2="{G[0]}" y2="{G[1]}" stroke="#111" stroke-width="2"/>
  <rect x="{A[0]}" y="{A[1]-14}" width="14" height="14" fill="none" stroke="#111"/>
  <rect x="{E[0]-14}" y="{E[1]-14}" width="14" height="14" fill="none" stroke="#111"/>
  <text x="{A[0]-16}" y="{A[1]+18}" font-family="Georgia, serif" font-size="14">A</text>
  <text x="{B[0]-16}" y="{B[1]-4}" font-family="Georgia, serif" font-size="14">B</text>
  <text x="{C[0]-4}" y="{C[1]-8}" font-family="Georgia, serif" font-size="14">C</text>
  <text x="{D[0]+6}" y="{D[1]-4}" font-family="Georgia, serif" font-size="14">D</text>
  <text x="{E[0]+6}" y="{E[1]+18}" font-family="Georgia, serif" font-size="14">E</text>
  <text x="{F[0]-4}" y="{F[1]+18}" font-family="Georgia, serif" font-size="14">F</text>
  <text x="{G[0]-4}" y="{G[1]+18}" font-family="Georgia, serif" font-size="14">G</text>
  <text x="{W/2}" y="{H-10}" text-anchor="middle" font-family="Arial" font-size="12">Note: Figure not drawn to scale.</text>
</svg>'''


def triangle_abc() -> str:
    W, H = 280, 220
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="140,30 40,180 240,180" fill="none" stroke="#111" stroke-width="2"/>
  <text x="132" y="24" font-family="Georgia, serif" font-size="16">B</text>
  <text x="24" y="198" font-family="Georgia, serif" font-size="16">A</text>
  <text x="244" y="198" font-family="Georgia, serif" font-size="16">C</text>
  <text x="{W/2}" y="{H-8}" text-anchor="middle" font-family="Arial" font-size="12">Note: Figure not drawn to scale.</text>
</svg>'''


def cell_phone_graph() -> str:
    W, H = 420, 320
    pad_l, pad_r, pad_t, pad_b = 70, 30, 30, 55
    plot_w, plot_h = W - pad_l - pad_r, H - pad_t - pad_b
    xmax, ymax = 10, 1800

    def sx(x: float) -> float:
        return pad_l + (x / xmax) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / ymax) * plot_h

    grid = []
    for x in range(0, 11, 2):
        grid.append(f'<line x1="{sx(x)}" y1="{pad_t}" x2="{sx(x)}" y2="{pad_t+plot_h}" stroke="#e5e7eb"/>')
        grid.append(f'<text x="{sx(x)}" y="{pad_t+plot_h+18}" text-anchor="middle" font-family="Arial" font-size="11">{x}</text>')
    for y in range(0, 1801, 300):
        grid.append(f'<line x1="{pad_l}" y1="{sy(y)}" x2="{pad_l+plot_w}" y2="{sy(y)}" stroke="#e5e7eb"/>')
        if y > 0:
            label = f"{y:,}"
            grid.append(f'<text x="{pad_l-8}" y="{sy(y)+4}" text-anchor="end" font-family="Arial" font-size="11">{label}</text>')

    # exponential through (0,370),(5,811),(10,1779)
    pts = []
    for i in range(0, 101):
        x = 10 * i / 100
        # fit a*b^x roughly
        y = 370 * ((1779 / 370) ** (x / 10))
        pts.append(f"{sx(x):.2f},{sy(y):.2f}")
    curve = f'<polyline points="{" ".join(pts)}" fill="none" stroke="#111" stroke-width="2.5"/>'
    axes = (
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  {axes}
  {curve}
  <text x="{pad_l+plot_w/2}" y="{H-12}" text-anchor="middle" font-family="Arial" font-size="13">Years since 1990</text>
  <text x="18" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="Arial" font-size="13" transform="rotate(-90 18 {pad_t+plot_h/2})">Cell phone subscribers</text>
</svg>'''


def td_scatter() -> str:
    W, H = 400, 340
    pad_l, pad_r, pad_t, pad_b = 55, 35, 30, 45
    plot_w, plot_h = W - pad_l - pad_r, H - pad_t - pad_b
    t0, t1, d0, d1 = 230, 270, 245, 525

    def sx(t: float) -> float:
        return pad_l + ((t - t0) / (t1 - t0)) * plot_w

    def sy(d: float) -> float:
        return pad_t + ((d1 - d) / (d1 - d0)) * plot_h

    grid = []
    for t in range(230, 271, 10):
        grid.append(f'<line x1="{sx(t)}" y1="{pad_t}" x2="{sx(t)}" y2="{pad_t+plot_h}" stroke="#eee"/>')
        grid.append(f'<text x="{sx(t)}" y="{pad_t+plot_h+16}" text-anchor="middle" font-family="Arial" font-size="11">{t}</text>')
    for d in range(245, 526, 35):
        grid.append(f'<line x1="{pad_l}" y1="{sy(d)}" x2="{pad_l+plot_w}" y2="{sy(d)}" stroke="#eee"/>')
        grid.append(f'<text x="{pad_l-6}" y="{sy(d)+4}" text-anchor="end" font-family="Arial" font-size="10">{d}</text>')
    line = f'<line x1="{sx(230)}" y1="{sy(403)}" x2="{sx(265)}" y2="{sy(473)}" stroke="#111" stroke-width="2"/>'
    pts = [(232, 390), (238, 420), (245, 430), (250, 450), (255, 455), (260, 470), (268, 490)]
    dots = "".join(f'<circle cx="{sx(t)}" cy="{sy(d)}" r="4" fill="#111"/>' for t, d in pts)
    axes = (
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  {axes}
  {line}
  {dots}
  <text x="{pad_l+plot_w+8}" y="{pad_t+plot_h}" font-family="Arial" font-size="13" font-style="italic">t</text>
  <text x="{pad_l+8}" y="{pad_t+12}" font-family="Arial" font-size="13" font-style="italic">d</text>
</svg>'''


def main() -> None:
    # Ensure English tables exist (may already be present)
    write(
        "eng1-q10-table.svg",
        table_svg(
            "Cumulative Counts of Fish in Three Taiwanese Tide Pools, 1999–2018",
            ["Species", "Station 1", "Station 2", "Station 3"],
            [
                ["striated rockskipper", "41", "39", "47"],
                ["blackspot sergeant", "338", "261", "136"],
                ["rippled rockskipper", "453", "360", "247"],
                ["Bengal sergeant", "123", "58", "48"],
            ],
            col_widths=[180, 100, 100, 100],
        ),
    )
    write(
        "eng1-q13-table.svg",
        table_svg(
            "Myoglobin (Mb) Levels in the Cardiac Tissue of Three Teleost Species",
            ["Species", "Heart tissue color", "Average Mb level", "Standard deviation of Mb level", "Number of healthy fish observed"],
            [
                ["Danio rerio", "red", "10.45", "1.16", "3"],
                ["Gnathonemus petersii", "red", "13.58", "2.25", "4"],
                ["Pantodon buchholzi", "white", "0.02", "0.01", "4"],
            ],
            col_widths=[160, 130, 120, 160, 160],
        ),
    )

    write("m1-q01.svg", w_curve_graph())
    write(
        "m1-q09.svg",
        table_svg("", ["h", "f(h)"], [["1", "125"], ["3", "225"]], col_widths=[80, 100]),
    )
    write("m1-q11.svg", right_triangle_abc())
    write("m1-q15.svg", scatter_lobf())
    write("m1-q21.svg", overlapping_triangles())

    write("math2-q02-triangle-abc.svg", triangle_abc())
    write(
        "math2-q07-gx-table.svg",
        table_svg(
            "",
            ["x", "g(x)"],
            [["1", "44"], ["2", "38"], ["3", "32"], ["4", "26"]],
            col_widths=[80, 90],
        ),
    )
    write("math2-q16-cell-phone-subscribers.svg", cell_phone_graph())
    write("math2-q19-td-scatter.svg", td_scatter())
    write(
        "math2-q20-cylinder-volumes.svg",
        table_svg(
            "",
            ["", "Volume (cubic units)"],
            [
                ["Right circular cylinder A", "32π"],
                ["Right circular cylinder B", "4,000π"],
            ],
            col_widths=[220, 160],
            blank_first_header=True,
        ),
    )
    write(
        "math2-q22-xy-table.svg",
        table_svg("", ["x", "y"], [["16", "−4"], ["18", "12"], ["20", "−4"]], col_widths=[80, 80]),
    )


if __name__ == "__main__":
    main()
