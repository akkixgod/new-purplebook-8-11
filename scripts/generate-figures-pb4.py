#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for PurpleBook test 4 (ElitePractice X4)."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/purplebook-test-4/figures")
OUT.mkdir(parents=True, exist_ok=True)


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
    font_size: int = 11,
    row_h: int = 36,
) -> str:
    widths = col_widths
    width = sum(widths) + 40
    title_h = 56 if title else 16
    height = title_h + 20 + row_h * (1 + len(rows)) + 16
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


def eng1_q12_grapevine_leaves() -> str:
    W, H = 520, 400
    pad_l, pad_r, pad_t, pad_b = 70, 30, 50, 100
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    groups = ["opposite side", "same side"]
    series = ["Amur grape", "July grape", "graybark grape"]
    data = {
        "Amur grape": [150, 60],
        "July grape": [200, 100],
        "graybark grape": [270, 90],
    }
    colors = {
        "Amur grape": "#6b7280",
        "July grape": "#d1d5db",
        "graybark grape": "#111",
    }
    y_max = 300
    parts = [
        f'<text x="{W/2}" y="28" text-anchor="middle" font-family="Arial" font-size="13" font-weight="700">Orientation of Leaf Pairs in Grapevines</text>',
        f'<text x="18" y="{(pad_t+H-pad_b)/2}" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-90 18 {(pad_t+H-pad_b)/2})">Number of pairs</text>',
    ]
    for v in range(0, 301, 50):
        y = pad_t + plot_h - (v / y_max) * plot_h
        parts.append(
            f'<line x1="{pad_l}" y1="{y}" x2="{W-pad_r}" y2="{y}" stroke="#e5e7eb"/>'
            f'<text x="{pad_l-8}" y="{y+4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{H-pad_b}" stroke="#111"/>'
        f'<line x1="{pad_l}" y1="{H-pad_b}" x2="{W-pad_r}" y2="{H-pad_b}" stroke="#111"/>'
    )
    gw = plot_w / 2
    bw = gw * 0.18
    for gi, g in enumerate(groups):
        gx = pad_l + gi * gw
        for si, s in enumerate(series):
            val = data[s][gi]
            h = (val / y_max) * plot_h
            x = gx + gw * 0.18 + si * (bw + 6)
            parts.append(
                f'<rect x="{x}" y="{pad_t + plot_h - h}" width="{bw}" height="{h}" fill="{colors[s]}" stroke="#111"/>'
            )
        parts.append(
            f'<text x="{gx + gw/2}" y="{H-pad_b+22}" text-anchor="middle" font-family="Arial" font-size="12">{g}</text>'
        )
    parts.append(
        f'<text x="{W/2}" y="{H-pad_b+44}" text-anchor="middle" font-family="Arial" font-size="12">Orientation of leaves in pair</text>'
    )
    lx = pad_l + 20
    ly = H - 42
    for i, s in enumerate(series):
        x = lx + i * 150
        parts.append(
            f'<rect x="{x}" y="{ly}" width="12" height="12" fill="{colors[s]}" stroke="#111"/>'
            f'<text x="{x+18}" y="{ly+11}" font-family="Arial" font-size="11">{s}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def eng2_q11_tribal_nations() -> str:
    return table_svg(
        "Total Areas of Five Tribal Nations around the United States",
        ["Tribal nation", "Location", "Area (square miles)"],
        [
            ["Crow Tribe", "Montana", "3,606"],
            ["White Earth Nation", "Minnesota", "1,167"],
            ["Tohono O'odham Nation", "Arizona", "4,453"],
            ["Choctaw Nation", "Oklahoma", "10,864"],
            ["Yakama Nation", "Washington", "2,188"],
        ],
        [200, 120, 140],
    )


def eng2_q12_painting_correlation() -> str:
    W, H = 540, 400
    pad_l, pad_r, pad_t, pad_b = 70, 30, 70, 100
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    groups = ["Impressionist", "Color field"]
    series = ["P1", "P3", "P6"]
    data = {"P1": [0.58, 0.14], "P3": [0.42, 0.11], "P6": [0.38, 0.11]}
    colors = {"P1": "#6b7280", "P3": "#d1d5db", "P6": "#111"}
    y_max = 0.6
    parts = [
        f'<text x="{W/2}" y="22" text-anchor="middle" font-family="Arial" font-size="12" font-weight="700">Correlation between Model-Predicted and Participant-Reported</text>',
        f'<text x="{W/2}" y="40" text-anchor="middle" font-family="Arial" font-size="12" font-weight="700">Enjoyment Ratings, by Painting Style</text>',
        f'<text x="18" y="{(pad_t+H-pad_b)/2}" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-90 18 {(pad_t+H-pad_b)/2})">Correlation</text>',
    ]
    for i in range(0, 7):
        v = i / 10
        y = pad_t + plot_h - (v / y_max) * plot_h
        parts.append(
            f'<line x1="{pad_l}" y1="{y}" x2="{W-pad_r}" y2="{y}" stroke="#e5e7eb"/>'
            f'<text x="{pad_l-8}" y="{y+4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{H-pad_b}" stroke="#111"/>'
        f'<line x1="{pad_l}" y1="{H-pad_b}" x2="{W-pad_r}" y2="{H-pad_b}" stroke="#111"/>'
    )
    gw = plot_w / 2
    bw = gw * 0.18
    for gi, g in enumerate(groups):
        gx = pad_l + gi * gw
        for si, s in enumerate(series):
            val = data[s][gi]
            h = (val / y_max) * plot_h
            x = gx + gw * 0.18 + si * (bw + 6)
            parts.append(
                f'<rect x="{x}" y="{pad_t + plot_h - h}" width="{bw}" height="{h}" fill="{colors[s]}" stroke="#111"/>'
            )
        parts.append(
            f'<text x="{gx + gw/2}" y="{H-pad_b+22}" text-anchor="middle" font-family="Arial" font-size="12">{g}</text>'
        )
    parts.append(
        f'<text x="{W/2}" y="{H-pad_b+44}" text-anchor="middle" font-family="Arial" font-size="12">Painting style</text>'
    )
    lx = pad_l + 80
    ly = H - 42
    for i, s in enumerate(series):
        x = lx + i * 100
        parts.append(
            f'<rect x="{x}" y="{ly}" width="12" height="12" fill="{colors[s]}" stroke="#111"/>'
            f'<text x="{x+18}" y="{ly+11}" font-family="Arial" font-size="11">{s}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q14_similar_triangles() -> str:
    # Smaller △ABC left; larger △A'B'C' right (same orientation, visibly larger)
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="560" height="280" viewBox="0 0 560 280">
  <rect width="100%" height="100%" fill="#fff"/>
  <!-- small triangle ABC: A bottom-left, B top (leftish), C bottom-right -->
  <polygon points="40,210 90,70 180,210" fill="none" stroke="#111" stroke-width="2"/>
  <text x="28" y="230" font-family="Arial" font-size="16" font-style="italic">A</text>
  <text x="82" y="58" font-family="Arial" font-size="16" font-style="italic">B</text>
  <text x="184" y="230" font-family="Arial" font-size="16" font-style="italic">C</text>
  <!-- large triangle A'B'C' -->
  <polygon points="260,230 360,40 520,230" fill="none" stroke="#111" stroke-width="2"/>
  <text x="242" y="252" font-family="Arial" font-size="16" font-style="italic">A′</text>
  <text x="348" y="28" font-family="Arial" font-size="16" font-style="italic">B′</text>
  <text x="524" y="252" font-family="Arial" font-size="16" font-style="italic">C′</text>
  <text x="280" y="270" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math1_q16_circle_a() -> str:
    W, H = 420, 400
    pad_l, pad_r, pad_t, pad_b = 40, 30, 20, 30
    x0, x1, y0, y1 = -4.0, 6.0, -2.0, 14.0

    def sx(x: float) -> float:
        return pad_l + (x - x0) / (x1 - x0) * (W - pad_l - pad_r)

    def sy(y: float) -> float:
        return pad_t + (y1 - y) / (y1 - y0) * (H - pad_t - pad_b)

    # unit length in svg for radius √7 ≈ 2.64575
    unit = (W - pad_l - pad_r) / (x1 - x0)
    r = (7**0.5) * unit
    parts: list[str] = []
    for i in range(-4, 7):
        parts.append(
            f'<line x1="{sx(i)}" y1="{sy(y1)}" x2="{sx(i)}" y2="{sy(y0)}" stroke="#e5e7eb"/>'
        )
    for j in range(-2, 15):
        parts.append(
            f'<line x1="{sx(x0)}" y1="{sy(j)}" x2="{sx(x1)}" y2="{sy(j)}" stroke="#e5e7eb"/>'
        )
    parts.append(
        f'<line x1="{sx(x0)}" y1="{sy(0)}" x2="{sx(x1)}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{sx(0)}" y1="{sy(y1)}" x2="{sx(0)}" y2="{sy(y0)}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<polygon points="{sx(x1)},{sy(0)} {sx(x1)-10},{sy(0)-5} {sx(x1)-10},{sy(0)+5}" fill="#111"/>'
        f'<polygon points="{sx(0)},{sy(y1)} {sx(0)-5},{sy(y1)+10} {sx(0)+5},{sy(y1)+10}" fill="#111"/>'
        f'<text x="{sx(x1)+8}" y="{sy(0)+4}" font-family="Arial" font-size="14" font-style="italic">x</text>'
        f'<text x="{sx(0)+8}" y="{sy(y1)+14}" font-family="Arial" font-size="14" font-style="italic">y</text>'
    )
    for i in [-4, -2, 2, 4, 6]:
        parts.append(
            f'<text x="{sx(i)}" y="{sy(0)+16}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>'
        )
    for j in range(2, 15, 2):
        parts.append(
            f'<text x="{sx(0)-8}" y="{sy(j)+4}" text-anchor="end" font-family="Arial" font-size="11">{j}</text>'
        )
    parts.append(
        f'<circle cx="{sx(0)}" cy="{sy(5)}" r="{r}" fill="none" stroke="#111" stroke-width="2"/>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q17_cherry_scatter() -> str:
    W, H = 480, 400
    pad_l, pad_r, pad_t, pad_b = 70, 30, 30, 70
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    x0, x1, y0, y1 = 0.0, 10.0, 0.0, 70.0

    def sx(x: float) -> float:
        return pad_l + (x - x0) / (x1 - x0) * plot_w

    def sy(y: float) -> float:
        return pad_t + (y1 - y) / (y1 - y0) * plot_h

    # Approx points from page; sum ≈ 231 (choice A)
    points = [(1, 5), (2, 10), (3, 16), (4, 20), (5, 32), (6, 40), (7, 52), (8, 56)]
    parts: list[str] = []
    for i in range(0, 11):
        parts.append(
            f'<line x1="{sx(i)}" y1="{sy(y1)}" x2="{sx(i)}" y2="{sy(y0)}" stroke="#e5e7eb"/>'
        )
    for j in range(0, 71, 10):
        parts.append(
            f'<line x1="{sx(x0)}" y1="{sy(j)}" x2="{sx(x1)}" y2="{sy(j)}" stroke="#e5e7eb"/>'
            f'<text x="{pad_l-8}" y="{sy(j)+4}" text-anchor="end" font-family="Arial" font-size="11">{j}</text>'
        )
    parts.append(
        f'<line x1="{sx(x0)}" y1="{sy(0)}" x2="{sx(x1)}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{sx(0)}" y1="{sy(y1)}" x2="{sx(0)}" y2="{sy(y0)}" stroke="#111" stroke-width="1.5"/>'
        f'<polygon points="{sx(x1)},{sy(0)} {sx(x1)-10},{sy(0)-5} {sx(x1)-10},{sy(0)+5}" fill="#111"/>'
        f'<polygon points="{sx(0)},{sy(y1)} {sx(0)-5},{sy(y1)+10} {sx(0)+5},{sy(y1)+10}" fill="#111"/>'
    )
    for i in range(1, 11):
        parts.append(
            f'<text x="{sx(i)}" y="{sy(0)+16}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>'
        )
    for x, y in points:
        parts.append(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="4.5" fill="#111"/>')
    parts.append(
        f'<text x="{(pad_l+W-pad_r)/2}" y="{H-18}" text-anchor="middle" font-family="Arial" font-size="12">Growing season after transplantation</text>'
        f'<text x="18" y="{(pad_t+H-pad_b)/2}" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-90 18 {(pad_t+H-pad_b)/2})">Volume of cherries (quarts)</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math2_q02_inequality() -> str:
    W, H = 440, 400
    pad_l, pad_r, pad_t, pad_b = 40, 30, 20, 30
    x0, x1, y0, y1 = -6.0, 4.0, -2.0, 12.0

    def sx(x: float) -> float:
        return pad_l + (x - x0) / (x1 - x0) * (W - pad_l - pad_r)

    def sy(y: float) -> float:
        return pad_t + (y1 - y) / (y1 - y0) * (H - pad_t - pad_b)

    parts: list[str] = []
    for i in range(-6, 5):
        parts.append(
            f'<line x1="{sx(i)}" y1="{sy(y1)}" x2="{sx(i)}" y2="{sy(y0)}" stroke="#e5e7eb"/>'
        )
    for j in range(-2, 13):
        parts.append(
            f'<line x1="{sx(x0)}" y1="{sy(j)}" x2="{sx(x1)}" y2="{sy(j)}" stroke="#e5e7eb"/>'
        )
    # shade y > 3x + 7: clip to plot, polygon along line then up/left boundary
    # line from left edge: at x=-6, y=3*(-6)+7=-11 (below plot) → clip at bottom
    # at y=-2: -2 = 3x+7 → x = -3
    # at top y=12: 12=3x+7 → x=5/3 ≈ 1.67
    # at right x=4: y=19 (above plot)
    # shaded: left/above of line within bounds
    poly = [
        (sx(-6), sy(12)),
        (sx(5 / 3), sy(12)),
        (sx(-3), sy(-2)),
        (sx(-6), sy(-2)),
    ]
    pts = " ".join(f"{x},{y}" for x, y in poly)
    parts.append(f'<polygon points="{pts}" fill="#d1d5db" opacity="0.85"/>')
    # dashed line y=3x+7 across visible portion: from (-3,-2) to (5/3,12)
    parts.append(
        f'<line x1="{sx(-3)}" y1="{sy(-2)}" x2="{sx(5/3)}" y2="{sy(12)}" stroke="#111" stroke-width="2" stroke-dasharray="6 4"/>'
    )
    parts.append(
        f'<line x1="{sx(x0)}" y1="{sy(0)}" x2="{sx(x1)}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{sx(0)}" y1="{sy(y1)}" x2="{sx(0)}" y2="{sy(y0)}" stroke="#111" stroke-width="1.5"/>'
        f'<polygon points="{sx(x1)},{sy(0)} {sx(x1)-10},{sy(0)-5} {sx(x1)-10},{sy(0)+5}" fill="#111"/>'
        f'<polygon points="{sx(0)},{sy(y1)} {sx(0)-5},{sy(y1)+10} {sx(0)+5},{sy(y1)+10}" fill="#111"/>'
        f'<text x="{sx(x1)+8}" y="{sy(0)+4}" font-family="Arial" font-size="14" font-style="italic">x</text>'
        f'<text x="{sx(0)+8}" y="{sy(y1)+14}" font-family="Arial" font-size="14" font-style="italic">y</text>'
    )
    for i in range(-6, 5, 2):
        if i == 0:
            continue
        parts.append(
            f'<text x="{sx(i)}" y="{sy(0)+16}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>'
        )
    for j in range(-2, 13, 2):
        if j == 0:
            continue
        parts.append(
            f'<text x="{sx(0)-8}" y="{sy(j)+4}" text-anchor="end" font-family="Arial" font-size="11">{j}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math2_q04_dna_line() -> str:
    W, H = 480, 380
    pad_l, pad_r, pad_t, pad_b = 70, 30, 30, 60
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    x0, x1, y0, y1 = 0.0, 100.0, 60.0, 110.0

    def sx(x: float) -> float:
        return pad_l + (x - x0) / (x1 - x0) * plot_w

    def sy(y: float) -> float:
        return pad_t + (y1 - y) / (y1 - y0) * plot_h

    parts: list[str] = []
    for i in range(0, 101, 10):
        parts.append(
            f'<line x1="{sx(i)}" y1="{sy(y1)}" x2="{sx(i)}" y2="{sy(y0)}" stroke="#e5e7eb"/>'
        )
    for j in range(60, 111, 5):
        parts.append(
            f'<line x1="{sx(x0)}" y1="{sy(j)}" x2="{sx(x1)}" y2="{sy(j)}" stroke="#e5e7eb"/>'
        )
    for i in range(0, 101, 20):
        parts.append(
            f'<text x="{sx(i)}" y="{sy(y0)+16}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>'
        )
    for j in range(60, 111, 10):
        parts.append(
            f'<text x="{pad_l-8}" y="{sy(j)+4}" text-anchor="end" font-family="Arial" font-size="11">{j}</text>'
        )
    parts.append(
        f'<line x1="{sx(x0)}" y1="{sy(y0)}" x2="{sx(x1)}" y2="{sy(y0)}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{sx(x0)}" y1="{sy(y1)}" x2="{sx(x0)}" y2="{sy(y0)}" stroke="#111" stroke-width="1.5"/>'
    )
    # y = 0.4x + 64
    parts.append(
        f'<line x1="{sx(0)}" y1="{sy(64)}" x2="{sx(100)}" y2="{sy(104)}" stroke="#111" stroke-width="2.5"/>'
    )
    parts.append(
        f'<text x="{(pad_l+W-pad_r)/2}" y="{H-14}" text-anchor="middle" font-family="Arial" font-size="12">GC content (%)</text>'
        f'<text x="18" y="{(pad_t+H-pad_b)/2}" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-90 18 {(pad_t+H-pad_b)/2})">Melting temperature (°C)</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math2_q17_age_group_table() -> str:
    return table_svg(
        "",
        ["", "0–9 years", "10–19 years", "20+ years", "Total"],
        [
            ["Group A", "15", "18", "7", "40"],
            ["Group B", "6", "7", "27", "40"],
            ["Group C", "19", "15", "6", "40"],
            ["Total", "40", "40", "40", "120"],
        ],
        [90, 100, 110, 100, 80],
    )


def math2_q21_prism_points() -> str:
    W, H = 420, 420
    pad_l, pad_r, pad_t, pad_b = 40, 30, 20, 30
    x0, x1, y0, y1 = 0.0, 11.0, 0.0, 17.0

    def sx(x: float) -> float:
        return pad_l + (x - x0) / (x1 - x0) * (W - pad_l - pad_r)

    def sy(y: float) -> float:
        return pad_t + (y1 - y) / (y1 - y0) * (H - pad_t - pad_b)

    parts: list[str] = []
    for i in range(0, 12):
        parts.append(
            f'<line x1="{sx(i)}" y1="{sy(y1)}" x2="{sx(i)}" y2="{sy(y0)}" stroke="#e5e7eb"/>'
        )
    for j in range(0, 18):
        parts.append(
            f'<line x1="{sx(x0)}" y1="{sy(j)}" x2="{sx(x1)}" y2="{sy(j)}" stroke="#e5e7eb"/>'
        )
    parts.append(
        f'<line x1="{sx(x0)}" y1="{sy(0)}" x2="{sx(x1)}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{sx(0)}" y1="{sy(y1)}" x2="{sx(0)}" y2="{sy(y0)}" stroke="#111" stroke-width="1.5"/>'
        f'<polygon points="{sx(x1)},{sy(0)} {sx(x1)-10},{sy(0)-5} {sx(x1)-10},{sy(0)+5}" fill="#111"/>'
        f'<polygon points="{sx(0)},{sy(y1)} {sx(0)-5},{sy(y1)+10} {sx(0)+5},{sy(y1)+10}" fill="#111"/>'
        f'<text x="{sx(x1)+8}" y="{sy(0)+4}" font-family="Arial" font-size="14" font-style="italic">x</text>'
        f'<text x="{sx(0)+8}" y="{sy(y1)+14}" font-family="Arial" font-size="14" font-style="italic">y</text>'
    )
    for i in range(1, 11):
        parts.append(
            f'<text x="{sx(i)}" y="{sy(0)+16}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>'
        )
    for j in range(2, 17, 2):
        parts.append(
            f'<text x="{sx(0)-8}" y="{sy(j)+4}" text-anchor="end" font-family="Arial" font-size="11">{j}</text>'
        )
    for x, y in [(0, 15), (10, 8), (10, 3)]:
        parts.append(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="5" fill="#111"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def main() -> None:
    write("eng1-q12-grapevine-leaf-orientation.svg", eng1_q12_grapevine_leaves())
    write("eng2-q11-tribal-nations-areas.svg", eng2_q11_tribal_nations())
    write("eng2-q12-painting-style-correlation.svg", eng2_q12_painting_correlation())
    write("math1-q14-similar-triangles.svg", math1_q14_similar_triangles())
    write("math1-q16-circle-a.svg", math1_q16_circle_a())
    write("math1-q17-cherry-scatterplot.svg", math1_q17_cherry_scatter())
    write("math2-q02-inequality-graph.svg", math2_q02_inequality())
    write("math2-q04-dna-melting-line.svg", math2_q04_dna_line())
    write("math2-q17-age-group-table.svg", math2_q17_age_group_table())
    write("math2-q21-prism-points.svg", math2_q21_prism_points())
    print("done all purplebook-test-4 figures")


if __name__ == "__main__":
    main()
