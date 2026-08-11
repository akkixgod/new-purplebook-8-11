#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures (no watermarks) for 2026 March Int-B."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2026-march-int-b/figures")
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
    x0 = 20
    y0 = title_h

    header_cells = []
    body_cells = []
    x = x0
    for i, h in enumerate(headers):
        header_cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{row_h}" fill="#f3f4f6" stroke="#111" stroke-width="1"/>'
            f'<text x="{x + widths[i]/2}" y="{y0 + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="700">{h}</text>'
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


def candle_graph() -> str:
    # y = -0.25x + 13; axes 0-14
    W, H = 520, 420
    pad_l, pad_r, pad_t, pad_b = 70, 30, 30, 60
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b

    def sx(x: float) -> float:
        return pad_l + (x / 14) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((14 - y) / 14) * plot_h

    grid = []
    for i in range(0, 15):
        grid.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t+plot_h}" stroke="#e5e7eb" stroke-width="1"/>'
        )
        grid.append(
            f'<line x1="{pad_l}" y1="{sy(i)}" x2="{pad_l+plot_w}" y2="{sy(i)}" stroke="#e5e7eb" stroke-width="1"/>'
        )
    labels = []
    for i in range(0, 15, 2):
        labels.append(
            f'<text x="{sx(i)}" y="{pad_t+plot_h+22}" text-anchor="middle" font-family="Arial" font-size="12">{i}</text>'
        )
        labels.append(
            f'<text x="{pad_l-10}" y="{sy(i)+4}" text-anchor="end" font-family="Arial" font-size="12">{i}</text>'
        )

    x1, y1 = sx(0), sy(13)
    x2, y2 = sx(14), sy(13 - 0.25 * 14)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>
  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111" stroke-width="2.5"/>
  {"".join(labels)}
  <text x="{pad_l+plot_w/2}" y="{H-12}" text-anchor="middle" font-family="Arial" font-size="13">Time (hours)</text>
  <text x="18" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="Arial" font-size="13" transform="rotate(-90 18 {pad_t+plot_h/2})">Weight (ounces)</text>
</svg>'''


def triangle_fgh() -> str:
    # Right triangle: H at right angle bottom-right, G bottom-left 60°, F top, hypotenuse GF=68
    W, H = 420, 360
    # Place G left, H right, F up
    G = (60, 280)
    Hpt = (320, 280)
    F = (320, 60)  # visual right angle at H — wait if H is right angle, F should be above H and G left of H
    # Actually: H right angle bottom-right, G bottom-left with 60°, F top. Hypotenuse is FG.
    # If angle G=60 and H=90, angle F=30. Side opposite 60 is FH, adjacent GH.
    # Hypotenuse FG = 68.
    G = (80, 290)
    Hpt = (300, 290)
    # For 30-60-90 with right at H: FG hypotenuse, GH = 68/2=34, FH=34√3
    # Visual: F above H
    F = (300, 80)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="{F[0]},{F[1]} {G[0]},{G[1]} {Hpt[0]},{Hpt[1]}" fill="none" stroke="#111" stroke-width="2"/>
  <rect x="{Hpt[0]-14}" y="{Hpt[1]-14}" width="14" height="14" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="{G[0]-8}" y="{G[1]+22}" font-family="Arial" font-size="16" font-weight="700">G</text>
  <text x="{Hpt[0]+8}" y="{Hpt[1]+22}" font-family="Arial" font-size="16" font-weight="700">H</text>
  <text x="{F[0]+8}" y="{F[1]+8}" font-family="Arial" font-size="16" font-weight="700">F</text>
  <text x="{(F[0]+G[0])/2 - 20}" y="{(F[1]+G[1])/2}" font-family="Arial" font-size="15">68</text>
  <text x="{G[0]+28}" y="{G[1]-12}" font-family="Arial" font-size="14">60°</text>
  <text x="{W/2}" y="340" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def scatter_td() -> str:
    # Approximate scatter with line of best fit; t 230-270, d ~405-485
    W, H = 520, 400
    pad_l, pad_r, pad_t, pad_b = 70, 30, 30, 50
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    t_min, t_max = 230, 270
    d_min, d_max = 245, 525

    def sx(t: float) -> float:
        return pad_l + ((t - t_min) / (t_max - t_min)) * plot_w

    def sy(d: float) -> float:
        return pad_t + ((d_max - d) / (d_max - d_min)) * plot_h

    points = [(235, 395), (238, 420), (248, 440), (253, 460), (258, 475), (265, 495)]
    # line approx d = 2.02t - 60-ish → use 160.1+2.02t or similar; visually through cloud
    # Use endpoints of fit: (230, 405) to (270, 485)
    dots = "".join(
        f'<circle cx="{sx(t)}" cy="{sy(d)}" r="5" fill="#111"/>' for t, d in points
    )
    y_ticks = list(range(245, 526, 35))
    t_ticks = list(range(230, 271, 10))
    grid = []
    labels = []
    for t in t_ticks:
        grid.append(f'<line x1="{sx(t)}" y1="{pad_t}" x2="{sx(t)}" y2="{pad_t+plot_h}" stroke="#e5e7eb"/>')
        labels.append(f'<text x="{sx(t)}" y="{pad_t+plot_h+20}" text-anchor="middle" font-family="Arial" font-size="11">{t}</text>')
    for d in y_ticks:
        grid.append(f'<line x1="{pad_l}" y1="{sy(d)}" x2="{pad_l+plot_w}" y2="{sy(d)}" stroke="#e5e7eb"/>')
        labels.append(f'<text x="{pad_l-8}" y="{sy(d)+4}" text-anchor="end" font-family="Arial" font-size="11">{d}</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111" stroke-width="1.5"/>
  <line x1="{sx(230)}" y1="{sy(405)}" x2="{sx(270)}" y2="{sy(485)}" stroke="#111" stroke-width="2"/>
  {dots}
  {"".join(labels)}
  <text x="{pad_l+plot_w/2}" y="{H-10}" text-anchor="middle" font-family="Arial" font-size="14" font-style="italic">t</text>
  <text x="18" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="Arial" font-size="14" font-style="italic" transform="rotate(-90 18 {pad_t+plot_h/2})">d</text>
</svg>'''


def inequality_choices() -> str:
    """Four dashed-line shaded graphs labeled A–D for 4x+5y<9 (y < -0.8x + 1.8)."""
    # Correct answer should be dashed line with negative slope, shade below-left.
    # Recreate the 4 options as on the test (vision said various slopes).
    def one(label: str, slope: float, intercept: float, shade_below: bool, ox: float) -> str:
        size = 220
        pad = 20
        # map -10..10 to pad..size-pad
        def s(v: float) -> float:
            return pad + ((v + 10) / 20) * (size - 2 * pad)

        # line from x=-10 to 10
        x1, x2 = -10.0, 10.0
        y1, y2 = slope * x1 + intercept, slope * x2 + intercept
        # clip visually
        path = f"M {s(x1)} {s(-y1)} L {s(x2)} {s(-y2)}"  # flip y
        # shade polygon - simplified half-plane
        if shade_below:
            poly = f"{s(x1)},{s(-y1)} {s(x2)},{s(-y2)} {s(10)},{s(-10)} {s(-10)},{s(-10)}"
        else:
            poly = f"{s(x1)},{s(-y1)} {s(x2)},{s(-y2)} {s(10)},{s(10)} {s(-10)},{s(10)}"
        ticks = "".join(
            f'<line x1="{s(i)}" y1="{s(-10)}" x2="{s(i)}" y2="{s(10)}" stroke="#eee"/>'
            f'<line x1="{s(-10)}" y1="{s(-i)}" x2="{s(10)}" y2="{s(-i)}" stroke="#eee"/>'
            for i in range(-10, 11, 2)
        )
        return f'''
  <g transform="translate({ox},30)">
    <text x="0" y="-8" font-family="Arial" font-size="16" font-weight="700">{label}</text>
    <rect x="0" y="0" width="{size}" height="{size}" fill="#fff" stroke="#ddd"/>
    {ticks}
    <line x1="{s(0)}" y1="{s(-10)}" x2="{s(0)}" y2="{s(10)}" stroke="#111"/>
    <line x1="{s(-10)}" y1="{s(0)}" x2="{s(10)}" y2="{s(0)}" stroke="#111"/>
    <polygon points="{poly}" fill="#d1d5db" fill-opacity="0.7"/>
    <path d="{path}" fill="none" stroke="#111" stroke-width="2" stroke-dasharray="6 4"/>
  </g>'''

    # Options matching typical SAT inequality for 4x+5y<9 ≈ y < -0.8x+1.8
    panels = [
        one("A)", 1.0, 2.0, True, 20),
        one("B)", 1.0, 2.0, False, 270),
        one("C)", -1.0, 2.0, False, 520),
        one("D)", -0.8, 1.8, True, 770),
    ]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1020" height="280" viewBox="0 0 1020 280">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(panels)}
</svg>'''


def bar_chart_4720() -> str:
    W, H = 640, 420
    pad_l, pad_r, pad_t, pad_b = 50, 30, 50, 90
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    cats = [
        ("self-dealing", [7, 8, 9]),
        ("undistributed income", [90, 89, 88]),
        ("taxable expenditures", [3, 3, 3]),
        ("excess business holdings", [1, 1, 1]),
    ]
    colors = ["#4b5563", "#9ca3af", "#111827"]
    group_w = plot_w / len(cats)
    bars = []
    labels = []
    for i, (name, vals) in enumerate(cats):
        gx = pad_l + i * group_w + group_w * 0.15
        bw = group_w * 0.2
        for j, v in enumerate(vals):
            h = (v / 100) * plot_h
            x = gx + j * (bw + 4)
            y = pad_t + plot_h - h
            bars.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" fill="{colors[j]}"/>')
        labels.append(
            f'<text x="{pad_l + i * group_w + group_w/2}" y="{H-45}" text-anchor="middle" font-family="Arial" font-size="11">{name}</text>'
        )
    y_labels = "".join(
        f'<text x="{pad_l-8}" y="{pad_t + plot_h - (v/100)*plot_h + 4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>'
        f'<line x1="{pad_l}" y1="{pad_t + plot_h - (v/100)*plot_h}" x2="{pad_l+plot_w}" y2="{pad_t + plot_h - (v/100)*plot_h}" stroke="#e5e7eb"/>'
        for v in range(0, 101, 10)
    )
    legend = (
        f'<rect x="{pad_l}" y="{H-22}" width="12" height="12" fill="{colors[0]}"/><text x="{pad_l+18}" y="{H-12}" font-family="Arial" font-size="11">2003</text>'
        f'<rect x="{pad_l+70}" y="{H-22}" width="12" height="12" fill="{colors[1]}"/><text x="{pad_l+88}" y="{H-12}" font-family="Arial" font-size="11">2004</text>'
        f'<rect x="{pad_l+140}" y="{H-22}" width="12" height="12" fill="{colors[2]}"/><text x="{pad_l+158}" y="{H-12}" font-family="Arial" font-size="11">2005</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <text x="{W/2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">Form 4720s Filed by Private Foundations, by Taxable Activity, 2003–2005</text>
  {y_labels}
  {"".join(bars)}
  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111"/>
  <line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111"/>
  {"".join(labels)}
  {legend}
</svg>'''


def main() -> None:
    write(
        "eng1-q10-table.svg",
        table_svg(
            "Minimum and Maximum Depths of Stony Coral Species in Caribbean and Indo-Pacific Waters",
            ["Species", "Minimum depth (meters)", "Maximum depth (meters)"],
            [
                ["Acropora echinata", "8", "25"],
                ["Danafungia scruposa", "1", "27"],
                ["Astreopora expansa", "5", "15"],
                ["Scolymia lacera", "10", "80"],
            ],
            [220, 180, 180],
        ),
    )
    write(
        "eng2-q11-table.svg",
        table_svg(
            "Global Strontium Seawater Curve",
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
    write("eng2-q13-graph.svg", bar_chart_4720())
    write("math1-q01-graph.svg", candle_graph())
    write("math1-q21-triangle.svg", triangle_fgh())
    write("math2-q15-scatter.svg", scatter_td())
    write("math2-q07-choices.svg", inequality_choices())


if __name__ == "__main__":
    main()
