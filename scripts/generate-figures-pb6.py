#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for PurpleBook test 6 (ElitePractice X6)."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/purplebook-test-6/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Georgia, serif"


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
            f'<text x="{x + widths[i] / 2}" y="{y0 + 24}" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700">{h}</text>'
        )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + row_h * (r + 1)
        x = x0
        for i, cell in enumerate(row):
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i] / 2}" y="{y + 24}" text-anchor="middle" font-family="{FONT}" font-size="13">{cell}</text>'
            )
            x += widths[i]
    title_el = (
        f'<text x="{width / 2}" y="28" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700">{title}</text>'
        if title
        else ""
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {title_el}
  {"".join(cells)}
</svg>'''


def eng1_q12_tide_pool() -> str:
    """Line graph: Fish Population in a Taiwanese Tide Pool."""
    W, H = 640, 480
    pad_l, pad_r, pad_t, pad_b = 80, 40, 70, 120
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    y_max = 65
    months = ["January 2001", "April 2001", "July 2001", "October 2001"]
    # combtooth blenny / yellowtail sergeant / rippled rockskipper
    series = [
        ("combtooth blenny", "solid", "triangle", [62, 1, 1, 1]),
        ("yellowtail sergeant", "dashed", "circle-open", [0, 3, 5, 13]),
        ("rippled rockskipper", "dotted", "circle-open-gray", [2, 5, 3, 2]),
    ]
    dash = {"solid": None, "dashed": "7 5", "dotted": "2 4"}

    def sx(i: float) -> float:
        return pad_l + (i / 3) * plot_w

    def sy(v: float) -> float:
        return pad_t + ((y_max - v) / y_max) * plot_h

    parts = [
        f'<text x="{W / 2}" y="22" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700">Fish Population in a Taiwanese Tide Pool,</text>',
        f'<text x="{W / 2}" y="42" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700">January 2001 to October 2001</text>',
        f'<text x="18" y="{(pad_t + H - pad_b) / 2}" text-anchor="middle" font-family="{FONT}" font-size="12" transform="rotate(-90 18 {(pad_t + H - pad_b) / 2})">Number of individual fish observed</text>',
    ]
    for v in range(0, 66, 5):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(v)}" x2="{W - pad_r}" y2="{sy(v)}" stroke="#e5e7eb"/>'
            f'<text x="{pad_l - 8}" y="{sy(v) + 4}" text-anchor="end" font-family="{FONT}" font-size="11">{v}</text>'
        )
    for i, m in enumerate(months):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" stroke="#e5e7eb"/>'
            f'<text x="{sx(i)}" y="{H - pad_b + 18}" text-anchor="middle" font-family="{FONT}" font-size="11" transform="rotate(-28 {sx(i)} {H - pad_b + 18})">{m}</text>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{H - pad_b}" stroke="#111"/>'
        f'<line x1="{pad_l}" y1="{H - pad_b}" x2="{W - pad_r}" y2="{H - pad_b}" stroke="#111"/>'
        f'<text x="{W / 2}" y="{H - pad_b + 52}" text-anchor="middle" font-family="{FONT}" font-size="12">Month</text>'
    )

    def marker(kind: str, x: float, y: float) -> str:
        if kind == "triangle":
            return (
                f'<polygon points="{x},{y - 6} {x + 5.5},{y + 4.5} {x - 5.5},{y + 4.5}" '
                f'fill="#111" stroke="#111"/>'
            )
        if kind == "circle-open":
            return f'<circle cx="{x}" cy="{y}" r="4.5" fill="#fff" stroke="#111" stroke-width="1.5"/>'
        # gray open circle
        return f'<circle cx="{x}" cy="{y}" r="4.5" fill="#fff" stroke="#6b7280" stroke-width="1.5"/>'

    for _name, style, mark, vals in series:
        pts = " ".join(f"{sx(i)},{sy(vals[i])}" for i in range(4))
        dashattr = f' stroke-dasharray="{dash[style]}"' if dash[style] else ""
        stroke = "#6b7280" if mark == "circle-open-gray" else "#111"
        parts.append(
            f'<polyline points="{pts}" fill="none" stroke="{stroke}" stroke-width="2"{dashattr}/>'
        )
        for i, v in enumerate(vals):
            parts.append(marker(mark, sx(i), sy(v)))

    ly = H - 28
    x = pad_l
    for name, style, mark, _vals in series:
        dashattr = f' stroke-dasharray="{dash[style]}"' if dash[style] else ""
        stroke = "#6b7280" if mark == "circle-open-gray" else "#111"
        parts.append(
            f'<line x1="{x}" y1="{ly}" x2="{x + 26}" y2="{ly}" stroke="{stroke}" stroke-width="2"{dashattr}/>'
        )
        parts.append(marker(mark, x + 13, ly))
        parts.append(f'<text x="{x + 34}" y="{ly + 4}" font-family="{FONT}" font-size="11">{name}</text>')
        x += 185
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def eng2_q11_strontium() -> str:
    return table_svg(
        "Strontium Isotope Ratios and Corresponding Numerical Ages in the Global Seawater Curve",
        ["⁸⁷Sr/⁸⁶Sr", "Age (Ma)"],
        [
            ["0.708980", "6.20"],
            ["0.709000", "5.86"],
            ["0.709020", "5.40"],
            ["0.709040", "4.75"],
            ["0.709060", "3.00"],
        ],
        [160, 120],
    )


def eng2_q12_mobility() -> str:
    """Grouped bar: mobility patterns US vs Côte d'Ivoire."""
    W, H = 660, 460
    pad_l, pad_r, pad_t, pad_b = 70, 30, 70, 120
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    y_max = 1.0
    cats = ["US 2", "US 3", "US 4", "CI 2", "CI 3", "CI 4"]
    # measured / density / preferences
    series = [
        ("measured", "#4b5563", [0.76, 0.12, 0.05, 0.80, 0.12, 0.04]),
        ("model: emphasis density", "#fff", [0.68, 0.19, 0.07, 0.85, 0.14, 0.03]),
        ("model: emphasis preferences", "#111", [0.47, 0.18, 0.09, 0.35, 0.21, 0.11]),
    ]
    parts = [
        f'<text x="{W / 2}" y="22" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700">Proportion of the Three Most Commonly Exhibited Mobility Patterns,</text>',
        f'<text x="{W / 2}" y="42" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700">in the US and Côte d\'Ivoire</text>',
        f'<text x="18" y="{(pad_t + H - pad_b) / 2}" text-anchor="middle" font-family="{FONT}" font-size="12" transform="rotate(-90 18 {(pad_t + H - pad_b) / 2})">Proportion</text>',
    ]
    for v in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        y = pad_t + plot_h - (v / y_max) * plot_h
        label = f"{v:g}" if v != 1.0 else "1"
        parts.append(
            f'<line x1="{pad_l}" y1="{y}" x2="{W - pad_r}" y2="{y}" stroke="#e5e7eb"/>'
            f'<text x="{pad_l - 8}" y="{y + 4}" text-anchor="end" font-family="{FONT}" font-size="11">{label}</text>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{H - pad_b}" stroke="#111"/>'
        f'<line x1="{pad_l}" y1="{H - pad_b}" x2="{W - pad_r}" y2="{H - pad_b}" stroke="#111"/>'
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{W - pad_r}" y2="{pad_t}" stroke="#111"/>'
    )
    gw = plot_w / 6
    bw = gw * 0.22
    for gi, cat in enumerate(cats):
        gx = pad_l + gi * gw
        for si, (_name, color, vals) in enumerate(series):
            val = vals[gi]
            h = (val / y_max) * plot_h
            x = gx + gw * 0.18 + si * (bw + 3)
            parts.append(
                f'<rect x="{x}" y="{pad_t + plot_h - h}" width="{bw}" height="{h}" fill="{color}" stroke="#111"/>'
            )
        parts.append(
            f'<text x="{gx + gw / 2}" y="{H - pad_b + 22}" text-anchor="middle" font-family="{FONT}" font-size="12">{cat}</text>'
        )
    parts.append(
        f'<text x="{W / 2}" y="{H - pad_b + 44}" text-anchor="middle" font-family="{FONT}" font-size="12">Mobility pattern by country</text>'
    )
    lx, ly = pad_l + 20, H - 42
    for i, (name, color, _) in enumerate(series):
        x = lx + i * 200
        parts.append(
            f'<rect x="{x}" y="{ly}" width="12" height="12" fill="{color}" stroke="#111"/>'
            f'<text x="{x + 18}" y="{ly + 11}" font-family="{FONT}" font-size="11">{name}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q15_tomato() -> str:
    """Scatterplot with LOBF; slope ~0.7 through origin."""
    W, H = 520, 460
    pad_l, pad_r, pad_t, pad_b = 70, 40, 30, 70
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    span = 500

    def sx(x: float) -> float:
        return pad_l + (x / span) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((span - y) / span) * plot_h

    points = [
        (50, 40),
        (120, 95),
        (160, 100),
        (200, 150),
        (250, 200),
        (300, 180),
        (350, 270),
        (400, 250),
        (450, 340),
        (480, 320),
    ]
    parts: list[str] = []
    for v in range(0, 501, 50):
        parts.append(
            f'<line x1="{sx(v)}" y1="{pad_t}" x2="{sx(v)}" y2="{pad_t + plot_h}" stroke="#e5e7eb"/>'
            f'<line x1="{pad_l}" y1="{sy(v)}" x2="{pad_l + plot_w}" y2="{sy(v)}" stroke="#e5e7eb"/>'
        )
    for v in range(0, 501, 100):
        parts.append(
            f'<text x="{sx(v)}" y="{pad_t + plot_h + 20}" text-anchor="middle" font-family="{FONT}" font-size="12">{v}</text>'
            f'<text x="{pad_l - 10}" y="{sy(v) + 4}" text-anchor="end" font-family="{FONT}" font-size="12">{v}</text>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{sx(0)}" y1="{sy(0)}" x2="{sx(500)}" y2="{sy(350)}" stroke="#111" stroke-width="2"/>'
    )
    for x, y in points:
        parts.append(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="4.5" fill="#111"/>')
    parts.append(
        f'<text x="{pad_l + plot_w / 2}" y="{H - 18}" text-anchor="middle" font-family="{FONT}" font-size="13">Number of tomato seeds planted</text>'
        f'<text x="16" y="{pad_t + plot_h / 2}" text-anchor="middle" font-family="{FONT}" font-size="12" transform="rotate(-90 16 {pad_t + plot_h / 2})">Number of tomato seeds that germinated</text>'
        f'<text x="{W - pad_r + 6}" y="{pad_t + plot_h + 4}" font-family="{FONT}" font-size="14" font-style="italic">x</text>'
        f'<text x="{pad_l + 8}" y="{pad_t + 14}" font-family="{FONT}" font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q16_ice_cream() -> str:
    W, H = 520, 220
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <rect x="20" y="20" width="200" height="70" fill="#f3f4f6" stroke="#111"/>
  <rect x="220" y="20" width="280" height="35" fill="#f3f4f6" stroke="#111"/>
  <rect x="220" y="55" width="140" height="35" fill="#f3f4f6" stroke="#111"/>
  <rect x="360" y="55" width="140" height="35" fill="#f3f4f6" stroke="#111"/>
  <text x="120" y="60" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700">Flavor of ice cream</text>
  <text x="360" y="42" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700">Type of topping</text>
  <text x="290" y="78" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700">Sprinkles</text>
  <text x="430" y="78" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700">No Sprinkles</text>
  <rect x="20" y="90" width="200" height="36" fill="#fff" stroke="#111"/>
  <rect x="220" y="90" width="140" height="36" fill="#fff" stroke="#111"/>
  <rect x="360" y="90" width="140" height="36" fill="#fff" stroke="#111"/>
  <text x="30" y="114" font-family="{FONT}" font-size="13">Chocolate</text>
  <text x="290" y="114" text-anchor="middle" font-family="{FONT}" font-size="13">60</text>
  <text x="430" y="114" text-anchor="middle" font-family="{FONT}" font-size="13">30</text>
  <rect x="20" y="126" width="200" height="36" fill="#fff" stroke="#111"/>
  <rect x="220" y="126" width="140" height="36" fill="#fff" stroke="#111"/>
  <rect x="360" y="126" width="140" height="36" fill="#fff" stroke="#111"/>
  <text x="30" y="150" font-family="{FONT}" font-size="13">Vanilla</text>
  <text x="290" y="150" text-anchor="middle" font-family="{FONT}" font-size="13">20</text>
  <text x="430" y="150" text-anchor="middle" font-family="{FONT}" font-size="13">30</text>
  <rect x="20" y="162" width="200" height="36" fill="#fff" stroke="#111"/>
  <rect x="220" y="162" width="140" height="36" fill="#fff" stroke="#111"/>
  <rect x="360" y="162" width="140" height="36" fill="#fff" stroke="#111"/>
  <text x="30" y="186" font-family="{FONT}" font-size="13">Twist</text>
  <text x="290" y="186" text-anchor="middle" font-family="{FONT}" font-size="13">80</text>
  <text x="430" y="186" text-anchor="middle" font-family="{FONT}" font-size="13">20</text>
</svg>'''


def math1_q20_nested_triangles() -> str:
    """Right triangle RST with nested XYZ; right angles at T and Y."""
    W, H = 420, 380
    # T bottom-left, R top, S bottom-right
    T = (70, 280)
    R = (70, 60)
    S = (340, 280)
    # X on RT, XY horizontal || TS, YZ vertical to Z on RS
    X = (70, 110)
    Y = (200, 110)
    z_y = 60 + (220 / 270) * (200 - 70)  # ≈ 165.9
    Z = (200, z_y)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="{R[0]},{R[1]} {T[0]},{T[1]} {S[0]},{S[1]}" fill="none" stroke="#111" stroke-width="2.5"/>
  <polygon points="{X[0]},{X[1]} {Y[0]},{Y[1]} {Z[0]},{Z[1]:.1f}" fill="none" stroke="#111" stroke-width="2"/>
  <rect x="{T[0]}" y="{T[1] - 16}" width="16" height="16" fill="none" stroke="#111" stroke-width="1.5"/>
  <rect x="{Y[0]}" y="{Y[1]}" width="14" height="14" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="{R[0] - 22}" y="{R[1] + 6}" font-family="{FONT}" font-size="16" font-weight="700">R</text>
  <text x="{S[0] + 10}" y="{S[1] + 6}" font-family="{FONT}" font-size="16" font-weight="700">S</text>
  <text x="{T[0] - 22}" y="{T[1] + 18}" font-family="{FONT}" font-size="16" font-weight="700">T</text>
  <text x="{X[0] - 22}" y="{X[1] + 6}" font-family="{FONT}" font-size="16" font-weight="700">X</text>
  <text x="{Y[0] + 8}" y="{Y[1] - 6}" font-family="{FONT}" font-size="16" font-weight="700">Y</text>
  <text x="{Z[0] + 10}" y="{Z[1] + 6}" font-family="{FONT}" font-size="16" font-weight="700">Z</text>
  <text x="{W / 2}" y="350" text-anchor="middle" font-family="{FONT}" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math2_q02_right_triangle() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="320" height="300" viewBox="0 0 320 300">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="70,240 70,60 230,240" fill="none" stroke="#111" stroke-width="2.5"/>
  <rect x="70" y="224" width="16" height="16" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="48" y="160" font-family="{FONT}" font-size="18">9</text>
  <text x="140" y="268" font-family="{FONT}" font-size="18">4</text>
  <text x="160" y="290" text-anchor="middle" font-family="{FONT}" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math2_q10_xy_table() -> str:
    # −5/9 as a stacked fraction in the cell
    W, H = 200, 180
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <rect x="20" y="16" width="80" height="36" fill="#f3f4f6" stroke="#111"/>
  <rect x="100" y="16" width="80" height="36" fill="#f3f4f6" stroke="#111"/>
  <text x="60" y="40" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="700">x</text>
  <text x="140" y="40" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="700">y</text>
  <rect x="20" y="52" width="80" height="40" fill="#fff" stroke="#111"/>
  <rect x="100" y="52" width="80" height="40" fill="#fff" stroke="#111"/>
  <text x="48" y="78" text-anchor="middle" font-family="{FONT}" font-size="14">−</text>
  <text x="68" y="70" text-anchor="middle" font-family="{FONT}" font-size="12">5</text>
  <line x1="58" y1="74" x2="78" y2="74" stroke="#111" stroke-width="1.2"/>
  <text x="68" y="88" text-anchor="middle" font-family="{FONT}" font-size="12">9</text>
  <text x="140" y="78" text-anchor="middle" font-family="{FONT}" font-size="14">0</text>
  <rect x="20" y="92" width="80" height="36" fill="#fff" stroke="#111"/>
  <rect x="100" y="92" width="80" height="36" fill="#fff" stroke="#111"/>
  <text x="60" y="116" text-anchor="middle" font-family="{FONT}" font-size="14">0</text>
  <text x="140" y="116" text-anchor="middle" font-family="{FONT}" font-size="14">−120</text>
  <rect x="20" y="128" width="80" height="36" fill="#fff" stroke="#111"/>
  <rect x="100" y="128" width="80" height="36" fill="#fff" stroke="#111"/>
  <text x="60" y="152" text-anchor="middle" font-family="{FONT}" font-size="14">6</text>
  <text x="140" y="152" text-anchor="middle" font-family="{FONT}" font-size="14">0</text>
</svg>'''


def math2_q11_line() -> str:
    """xy-plane line through (0,-4) and (2,0)."""
    W, H = 440, 440
    pad = 40
    span = 10  # -5..5

    def s(v: float) -> float:
        return pad + ((v + 5) / span) * (W - 2 * pad)

    def sy(v: float) -> float:
        return pad + ((5 - v) / span) * (H - 2 * pad)

    parts: list[str] = []
    for i in range(-5, 6):
        parts.append(
            f'<line x1="{s(i)}" y1="{sy(-5)}" x2="{s(i)}" y2="{sy(5)}" stroke="#e5e7eb"/>'
            f'<line x1="{s(-5)}" y1="{sy(i)}" x2="{s(5)}" y2="{sy(i)}" stroke="#e5e7eb"/>'
        )
    for i in range(-5, 6):
        if i == 0:
            continue
        parts.append(
            f'<text x="{s(i)}" y="{sy(0) + 16}" text-anchor="middle" font-family="{FONT}" font-size="12">{i}</text>'
            f'<text x="{s(0) - 12}" y="{sy(i) + 4}" text-anchor="end" font-family="{FONT}" font-size="12">{i}</text>'
        )
    # axes with arrows
    parts.append(
        f'<line x1="{s(-5)}" y1="{sy(0)}" x2="{s(5)}" y2="{sy(0)}" stroke="#111" stroke-width="1.5" marker-end="url(#arrow)"/>'
        f'<line x1="{s(0)}" y1="{sy(-5)}" x2="{s(0)}" y2="{sy(5)}" stroke="#111" stroke-width="1.5" marker-end="url(#arrow)"/>'
    )
    # line y = 2x - 4 from x=-0.5 to x=4.5 clipped to grid
    x1, x2 = -0.5, 4.5
    y1, y2 = 2 * x1 - 4, 2 * x2 - 4
    parts.append(
        f'<line x1="{s(x1)}" y1="{sy(y1)}" x2="{s(x2)}" y2="{sy(y2)}" stroke="#111" stroke-width="2.5"/>'
        f'<text x="{s(0) + 10}" y="{sy(0) + 16}" font-family="{FONT}" font-size="12" font-style="italic">O</text>'
        f'<text x="{s(5) - 14}" y="{sy(0) - 8}" font-family="{FONT}" font-size="14" font-style="italic">x</text>'
        f'<text x="{s(0) + 8}" y="{sy(5) + 14}" font-family="{FONT}" font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#111"/>
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math2_q14_copper() -> str:
    """First-quadrant line through (0,0) and (1000, 60)."""
    W, H = 520, 420
    pad_l, pad_r, pad_t, pad_b = 60, 40, 30, 50
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b

    def sx(x: float) -> float:
        return pad_l + (x / 1000) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((100 - y) / 100) * plot_h

    parts: list[str] = []
    for x in range(0, 1001, 100):
        parts.append(
            f'<line x1="{sx(x)}" y1="{pad_t}" x2="{sx(x)}" y2="{pad_t + plot_h}" stroke="#e5e7eb"/>'
        )
    for y in range(0, 101, 10):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(y)}" x2="{pad_l + plot_w}" y2="{sy(y)}" stroke="#e5e7eb"/>'
        )
    for x in range(200, 1001, 200):
        label = f"{x:,}" if x == 1000 else str(x)
        parts.append(
            f'<text x="{sx(x)}" y="{pad_t + plot_h + 20}" text-anchor="middle" font-family="{FONT}" font-size="12">{label}</text>'
        )
    for y in range(20, 101, 20):
        parts.append(
            f'<text x="{pad_l - 10}" y="{sy(y) + 4}" text-anchor="end" font-family="{FONT}" font-size="12">{y}</text>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{sx(0)}" y1="{sy(0)}" x2="{sx(1000)}" y2="{sy(60)}" stroke="#111" stroke-width="2.5"/>'
        f'<text x="{pad_l - 4}" y="{pad_t + plot_h + 16}" text-anchor="end" font-family="{FONT}" font-size="12" font-style="italic">O</text>'
        f'<text x="{W - pad_r + 6}" y="{pad_t + plot_h + 4}" font-family="{FONT}" font-size="14" font-style="italic">x</text>'
        f'<text x="{pad_l + 8}" y="{pad_t + 14}" font-family="{FONT}" font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math2_q17_parallels() -> str:
    """Parallel lines AB || CD with transversals AD, BC crossing at E; angles x,y,z."""
    W, H = 480, 360
    # Top line y=80, bottom y=260
    A, B = (100, 80), (380, 80)
    C, D = (100, 260), (380, 260)
    # AD from A to D, BC from B to C; intersection E
    # A(100,80)->D(380,260): param t, x=100+280t, y=80+180t
    # B(380,80)->C(100,260): x=380-280s, y=80+180s
    # 100+280t = 380-280s => 280t+280s=280 => t+s=1
    # 80+180t = 80+180s => t=s => t=0.5, s=0.5
    E = (100 + 140, 80 + 90)  # (240, 170)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <!-- parallels -->
  <line x1="60" y1="{A[1]}" x2="420" y2="{B[1]}" stroke="#111" stroke-width="2.5"/>
  <line x1="60" y1="{C[1]}" x2="420" y2="{D[1]}" stroke="#111" stroke-width="2.5"/>
  <!-- parallel arrow marks -->
  <polygon points="230,80 242,76 242,84" fill="#111"/>
  <polygon points="250,80 262,76 262,84" fill="#111"/>
  <polygon points="230,260 242,256 242,264" fill="#111"/>
  <polygon points="250,260 262,256 262,264" fill="#111"/>
  <!-- transversals -->
  <line x1="{A[0]}" y1="{A[1]}" x2="{D[0]}" y2="{D[1]}" stroke="#111" stroke-width="2.5"/>
  <line x1="{B[0]}" y1="{B[1]}" x2="{C[0]}" y2="{C[1]}" stroke="#111" stroke-width="2.5"/>
  <!-- angle arcs: y at B (obtuse, below-left of B along BA and BC), z at D, x at E (∠AEB) -->
  <path d="M {B[0] - 36},{B[1]} A 36 36 0 0 1 {B[0] - 22},{B[1] + 28}" fill="none" stroke="#111" stroke-width="1.3"/>
  <text x="{B[0] - 58}" y="{B[1] + 28}" font-family="{FONT}" font-size="15" font-style="italic">y</text>
  <path d="M {D[0] - 36},{D[1]} A 36 36 0 0 0 {D[0] - 22},{D[1] - 28}" fill="none" stroke="#111" stroke-width="1.3"/>
  <text x="{D[0] - 58}" y="{D[1] - 18}" font-family="{FONT}" font-size="15" font-style="italic">z</text>
  <path d="M {E[0] - 20},{E[1] - 16} A 26 26 0 0 1 {E[0] + 20},{E[1] - 16}" fill="none" stroke="#111" stroke-width="1.3"/>
  <text x="{E[0] - 4}" y="{E[1] - 28}" font-family="{FONT}" font-size="15" font-style="italic">x</text>
  <text x="{A[0] - 18}" y="{A[1] - 10}" font-family="{FONT}" font-size="15" font-weight="700">A</text>
  <text x="{B[0] + 8}" y="{B[1] - 10}" font-family="{FONT}" font-size="15" font-weight="700">B</text>
  <text x="{C[0] - 18}" y="{C[1] + 22}" font-family="{FONT}" font-size="15" font-weight="700">C</text>
  <text x="{D[0] + 8}" y="{D[1] + 22}" font-family="{FONT}" font-size="15" font-weight="700">D</text>
  <text x="{E[0] + 10}" y="{E[1] + 6}" font-family="{FONT}" font-size="15" font-weight="700">E</text>
  <text x="{W / 2}" y="330" text-anchor="middle" font-family="{FONT}" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math2_q21_scatter_quadratic() -> str:
    """Scatter with quadratic model; outlier at x=0."""
    W, H = 520, 440
    pad_l, pad_r, pad_t, pad_b = 50, 40, 30, 50
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    x0, x1, y0, y1 = -8.0, 8.0, 0.0, 14.0

    def sx(x: float) -> float:
        return pad_l + ((x - x0) / (x1 - x0)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((y1 - y) / (y1 - y0)) * plot_h

    def model(x: float) -> float:
        return 0.04 * x * x - 0.07 * x + 6.52

    points = [
        (-8, 10),
        (-6, 8),
        (-4, 7),
        (-2, 6.5),
        (0, 11.5),  # outlier
        (2, 6.5),
        (4, 7),
        (6, 8),
        (8, 10),
    ]
    parts: list[str] = []
    for i in range(-8, 9):
        parts.append(
            f'<line x1="{sx(i)}" y1="{sy(0)}" x2="{sx(i)}" y2="{sy(14)}" stroke="#e5e7eb"/>'
        )
    for j in range(0, 15):
        parts.append(
            f'<line x1="{sx(-8)}" y1="{sy(j)}" x2="{sx(8)}" y2="{sy(j)}" stroke="#e5e7eb"/>'
        )
    for i in range(-8, 9, 2):
        if i == 0:
            continue
        parts.append(
            f'<text x="{sx(i)}" y="{sy(0) + 16}" text-anchor="middle" font-family="{FONT}" font-size="12">{i}</text>'
        )
    for j in range(2, 15, 2):
        parts.append(
            f'<text x="{sx(0) - 10}" y="{sy(j) + 4}" text-anchor="end" font-family="{FONT}" font-size="12">{j}</text>'
        )
    parts.append(
        f'<line x1="{sx(-8)}" y1="{sy(0)}" x2="{sx(8)}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{sx(0)}" y1="{sy(0)}" x2="{sx(0)}" y2="{sy(14)}" stroke="#111" stroke-width="1.5"/>'
    )
    # parabola path
    curve_pts = []
    for k in range(0, 161):
        x = -8 + k * 16 / 160
        curve_pts.append(f"{sx(x):.1f},{sy(model(x)):.1f}")
    parts.append(
        f'<polyline points="{" ".join(curve_pts)}" fill="none" stroke="#111" stroke-width="2"/>'
    )
    for x, y in points:
        parts.append(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="4.5" fill="#111"/>')
    parts.append(
        f'<text x="{sx(8) - 10}" y="{sy(0) - 8}" font-family="{FONT}" font-size="14" font-style="italic">x</text>'
        f'<text x="{sx(0) + 8}" y="{sy(14) + 14}" font-family="{FONT}" font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def main() -> None:
    write("eng1-q12-tide-pool.svg", eng1_q12_tide_pool())
    write("eng2-q11-strontium-table.svg", eng2_q11_strontium())
    write("eng2-q12-mobility-bars.svg", eng2_q12_mobility())
    write("math1-q15-tomato-scatter.svg", math1_q15_tomato())
    write("math1-q16-ice-cream-table.svg", math1_q16_ice_cream())
    write("math1-q20-nested-triangles.svg", math1_q20_nested_triangles())
    write("math2-q02-right-triangle.svg", math2_q02_right_triangle())
    write("math2-q10-xy-table.svg", math2_q10_xy_table())
    write("math2-q11-line-graph.svg", math2_q11_line())
    write("math2-q14-copper-resistivity.svg", math2_q14_copper())
    write("math2-q17-parallel-lines.svg", math2_q17_parallels())
    write("math2-q21-scatter-quadratic.svg", math2_q21_scatter_quadratic())
    print("done all purplebook-test-6 figures")


if __name__ == "__main__":
    main()
