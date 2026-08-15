#!/usr/bin/env python3
"""Generate Math Module 1 SVG figures for 2025-august-us-v2."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-august-us-v2/figures")
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
) -> str:
    n = len(headers)
    widths = col_widths or ([120] * n)
    width = sum(widths) + 40
    row_h = 36
    title_h = 56 if title else 16
    height = title_h + 40 + row_h * (1 + len(rows)) + 20
    x0, y0 = 20, title_h
    cells = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{row_h}" fill="#f3f4f6" stroke="#111" stroke-width="1"/>'
            f'<text x="{x + widths[i]/2}" y="{y0 + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="700">{esc(h)}</text>'
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


def w_curve() -> str:
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
        grid.append(
            f'<line x1="{sx(x)}" y1="{pad_t}" x2="{sx(x)}" y2="{pad_t+plot_h}" stroke="#eee"/>'
        )
        if x % 2 == 0:
            grid.append(
                f'<text x="{sx(x)}" y="{pad_t+plot_h+16}" text-anchor="middle" font-family="Arial" font-size="11">{x}</text>'
            )
    for y in range(ymin, ymax + 1):
        grid.append(
            f'<line x1="{pad_l}" y1="{sy(y)}" x2="{pad_l+plot_w}" y2="{sy(y)}" stroke="#eee"/>'
        )
        if y % 2 == 0:
            grid.append(
                f'<text x="{pad_l-8}" y="{sy(y)+4}" text-anchor="end" font-family="Arial" font-size="11">{y}</text>'
            )

    # mins (-7,2),(7,2), max (0,9) — shape ~ a(x^2-49)^2 + 2 with a so f(0)=9
    # a*2401 + 2 = 9 → a = 7/2401
    pts = []
    for i in range(0, 241):
        x = -10 + 20 * i / 240
        y = (7 / 2401) * (x * x - 49) ** 2 + 2
        if ymin - 0.2 <= y <= ymax + 0.5:
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
  <text x="{sx(0)+10}" y="{sy(0)-8}" font-family="Arial" font-size="12">O</text>
  <text x="{pad_l+plot_w+8}" y="{sy(0)}" font-family="Arial" font-size="13" font-style="italic">x</text>
  <text x="{sx(0)+8}" y="{pad_t+14}" font-family="Arial" font-size="13" font-style="italic">y</text>
</svg>'''


def scatter_lobf() -> str:
    W, H = 420, 380
    pad_l, pad_r, pad_t, pad_b = 45, 35, 25, 40
    plot_w, plot_h = W - pad_l - pad_r, H - pad_t - pad_b
    mx = 14

    def sx(x: float) -> float:
        return pad_l + (x / mx) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((mx - y) / mx) * plot_h

    grid = []
    for v in range(0, 15, 2):
        grid.append(f'<line x1="{sx(v)}" y1="{pad_t}" x2="{sx(v)}" y2="{pad_t+plot_h}" stroke="#e5e7eb"/>')
        grid.append(f'<line x1="{pad_l}" y1="{sy(v)}" x2="{pad_l+plot_w}" y2="{sy(v)}" stroke="#e5e7eb"/>')
        grid.append(
            f'<text x="{sx(v)}" y="{pad_t+plot_h+16}" text-anchor="middle" font-family="Arial" font-size="11">{v}</text>'
        )
        if v > 0:
            grid.append(
                f'<text x="{pad_l-8}" y="{sy(v)+4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>'
            )
    # y = 3.43 + 1.01x
    line = f'<line x1="{sx(0)}" y1="{sy(3.43)}" x2="{sx(10.5)}" y2="{sy(3.43+1.01*10.5)}" stroke="#111" stroke-width="2"/>'
    pts = [(1, 4.6), (3, 6.4), (5, 8.4), (7, 10.6), (9, 12.6)]
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


def right_triangle_abc() -> str:
    # A top, B bottom-right right angle, C bottom-left; AB=26 vertical, CA=41 hyp
    W, H = 360, 320
    Ax, Ay = 90, 40
    Bx, By = 90, 250
    Cx, Cy = 300, 250
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="{Ax},{Ay} {Bx},{By} {Cx},{Cy}" fill="none" stroke="#111" stroke-width="2"/>
  <rect x="{Bx}" y="{By-18}" width="18" height="18" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="{Ax-18}" y="{Ay+8}" font-family="Georgia, serif" font-size="16">A</text>
  <text x="{Bx-18}" y="{By+22}" font-family="Georgia, serif" font-size="16">B</text>
  <text x="{Cx+8}" y="{Cy+22}" font-family="Georgia, serif" font-size="16">C</text>
  <text x="{Ax-30}" y="{(Ay+By)/2+5}" font-family="Arial" font-size="14">26</text>
  <text x="{(Ax+Cx)/2+12}" y="{(Ay+Cy)/2}" font-family="Arial" font-size="14">41</text>
  <text x="{W/2}" y="{H-12}" text-anchor="middle" font-family="Arial" font-size="12">Note: Figure not drawn to scale.</text>
</svg>'''


def right_triangle_3_8() -> str:
    W, H = 320, 260
    # right at bottom-right; horizontal 8, vertical 3, hyp c
    Ax, Ay = 60, 200  # left
    Bx, By = 260, 200  # right angle
    Cx, Cy = 260, 80  # top
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="{Ax},{Ay} {Bx},{By} {Cx},{Cy}" fill="none" stroke="#111" stroke-width="2"/>
  <rect x="{Bx-18}" y="{By-18}" width="18" height="18" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="{(Ax+Bx)/2}" y="{Ay+22}" text-anchor="middle" font-family="Arial" font-size="14">8</text>
  <text x="{Bx+10}" y="{(By+Cy)/2}" font-family="Arial" font-size="14">3</text>
  <text x="{(Ax+Cx)/2-10}" y="{(Ay+Cy)/2}" font-family="Arial" font-size="14" font-style="italic">c</text>
  <text x="{W/2}" y="{H-10}" text-anchor="middle" font-family="Arial" font-size="12">Note: Figure not drawn to scale.</text>
</svg>'''


def overlapping_triangles() -> str:
    # Base G F E D left→right; A above G; C above D; hyp AE and CF meet at B
    W, H = 460, 300
    G, F, E, D = (70, 240), (170, 240), (290, 240), (390, 240)
    A, C = (70, 60), (390, 60)
    B = (230, 130)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <line x1="{G[0]}" y1="{G[1]}" x2="{D[0]}" y2="{D[1]}" stroke="#111" stroke-width="2"/>
  <line x1="{A[0]}" y1="{A[1]}" x2="{G[0]}" y2="{G[1]}" stroke="#111" stroke-width="2"/>
  <line x1="{A[0]}" y1="{A[1]}" x2="{E[0]}" y2="{E[1]}" stroke="#111" stroke-width="2"/>
  <line x1="{C[0]}" y1="{C[1]}" x2="{D[0]}" y2="{D[1]}" stroke="#111" stroke-width="2"/>
  <line x1="{C[0]}" y1="{C[1]}" x2="{F[0]}" y2="{F[1]}" stroke="#111" stroke-width="2"/>
  <rect x="{G[0]}" y="{G[1]-14}" width="14" height="14" fill="none" stroke="#111"/>
  <rect x="{D[0]-14}" y="{D[1]-14}" width="14" height="14" fill="none" stroke="#111"/>
  <text x="{A[0]-16}" y="{A[1]+4}" font-family="Georgia, serif" font-size="14">A</text>
  <text x="{B[0]-4}" y="{B[1]-8}" font-family="Georgia, serif" font-size="14">B</text>
  <text x="{C[0]+6}" y="{C[1]+4}" font-family="Georgia, serif" font-size="14">C</text>
  <text x="{D[0]+4}" y="{D[1]+18}" font-family="Georgia, serif" font-size="14">D</text>
  <text x="{E[0]-4}" y="{E[1]+18}" font-family="Georgia, serif" font-size="14">E</text>
  <text x="{F[0]-4}" y="{F[1]+18}" font-family="Georgia, serif" font-size="14">F</text>
  <text x="{G[0]-16}" y="{G[1]+18}" font-family="Georgia, serif" font-size="14">G</text>
  <text x="{W/2}" y="{H-12}" text-anchor="middle" font-family="Arial" font-size="12">Note: Figure not drawn to scale.</text>
</svg>'''


def main() -> None:
    write("m1-q01.svg", w_curve())
    write("m1-q05.svg", scatter_lobf())
    write(
        "m1-q10.svg",
        table_svg("", ["h", "f(h)"], [["1", "125"], ["3", "225"]], col_widths=[80, 100]),
    )
    write("m1-q11.svg", right_triangle_abc())
    write("m1-q19.svg", right_triangle_3_8())
    write("m1-q21.svg", overlapping_triangles())


if __name__ == "__main__":
    main()
