#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for PurpleBook test 5 (ElitePractice X5)."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/purplebook-test-5/figures")
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


def eng1_q10_lakes_ice() -> str:
    """Grouped bar: Days per Winter That Lakes Have Surface Ice."""
    W, H = 560, 420
    pad_l, pad_r, pad_t, pad_b = 70, 30, 70, 110
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    y_max = 200
    winters = ["1980–81", "2005–06"]
    # dark gray, light gray, black
    series = [
        ("Lake Baikal", "#4b5563", [95, 110]),
        ("Oulujärvi", "#d1d5db", [195, 155]),
        ("Lake Kegonsa", "#111", [94, 102]),
    ]
    parts = [
        f'<text x="{W / 2}" y="28" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700">Days per Winter That Lakes Have Surface Ice</text>',
        f'<text x="18" y="{(pad_t + H - pad_b) / 2}" text-anchor="middle" font-family="{FONT}" font-size="12" transform="rotate(-90 18 {(pad_t + H - pad_b) / 2})">Days</text>',
    ]
    for v in range(0, 201, 40):
        y = pad_t + plot_h - (v / y_max) * plot_h
        parts.append(
            f'<line x1="{pad_l}" y1="{y}" x2="{W - pad_r}" y2="{y}" stroke="#e5e7eb"/>'
            f'<text x="{pad_l - 8}" y="{y + 4}" text-anchor="end" font-family="{FONT}" font-size="11">{v}</text>'
        )
    parts.append(
        f'<rect x="{pad_l}" y="{pad_t}" width="{plot_w}" height="{plot_h}" fill="none" stroke="#111"/>'
    )
    gw = plot_w / 2
    bw = gw * 0.2
    for gi, winter in enumerate(winters):
        gx = pad_l + gi * gw
        for si, (_name, color, vals) in enumerate(series):
            val = vals[gi]
            h = (val / y_max) * plot_h
            x = gx + gw * 0.2 + si * (bw + 6)
            parts.append(
                f'<rect x="{x}" y="{pad_t + plot_h - h}" width="{bw}" height="{h}" fill="{color}" stroke="#111"/>'
            )
        parts.append(
            f'<text x="{gx + gw / 2}" y="{H - pad_b + 22}" text-anchor="middle" font-family="{FONT}" font-size="12">{winter}</text>'
        )
    parts.append(
        f'<text x="{W / 2}" y="{H - pad_b + 42}" text-anchor="middle" font-family="{FONT}" font-size="12">Winter</text>'
    )
    lx, ly = pad_l + 40, H - 42
    for i, (name, color, _) in enumerate(series):
        x = lx + i * 150
        parts.append(
            f'<rect x="{x}" y="{ly}" width="12" height="12" fill="{color}" stroke="#111"/>'
            f'<text x="{x + 18}" y="{ly + 11}" font-family="{FONT}" font-size="11">{name}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def eng1_q11_traffic_delay() -> str:
    """Line graph: Annual Average Hours of Highway Traffic Delay per Auto Commuter."""
    W, H = 620, 440
    pad_l, pad_r, pad_t, pad_b = 70, 30, 60, 120
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    years = [1990, 1992, 1994, 1996, 1998, 2000]
    y_max = 70

    def sx(year: float) -> float:
        return pad_l + ((year - 1990) / 10) * plot_w

    def sy(v: float) -> float:
        return pad_t + ((y_max - v) / y_max) * plot_h

    # Jacksonville solid + filled squares; Albuquerque dashed + open diamonds;
    # Boise dotted + open circles; NYC solid + filled circles
    series = [
        ("Jacksonville, Florida", "solid", "square", [22, 27, 30, 33, 37, 40]),
        ("Albuquerque, New Mexico", "dashed", "diamond", [24, 27, 30, 32, 34, 37]),
        ("Boise, Idaho", "dotted", "circle-open", [8, 12, 16, 19, 23, 27]),
        ("New York City, New York", "solid", "circle", [44, 48, 52, 56, 60, 63]),
    ]
    dash = {"solid": None, "dashed": "7 5", "dotted": "2 4"}
    parts = [
        f'<text x="{W / 2}" y="26" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700">Annual Average Hours of Highway Traffic Delay per Auto Commuter</text>',
        f'<text x="16" y="{(pad_t + H - pad_b) / 2}" text-anchor="middle" font-family="{FONT}" font-size="12" transform="rotate(-90 16 {(pad_t + H - pad_b) / 2})">Hours of delay</text>',
    ]
    for v in range(0, 71, 10):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(v)}" x2="{W - pad_r}" y2="{sy(v)}" stroke="#e5e7eb"/>'
            f'<text x="{pad_l - 8}" y="{sy(v) + 4}" text-anchor="end" font-family="{FONT}" font-size="11">{v}</text>'
        )
    for year in years:
        parts.append(
            f'<text x="{sx(year)}" y="{H - pad_b + 18}" text-anchor="middle" font-family="{FONT}" font-size="11">{year}</text>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{H - pad_b}" stroke="#111"/>'
        f'<line x1="{pad_l}" y1="{H - pad_b}" x2="{W - pad_r}" y2="{H - pad_b}" stroke="#111"/>'
    )
    parts.append(
        f'<text x="{W / 2}" y="{H - pad_b + 38}" text-anchor="middle" font-family="{FONT}" font-size="12">Year</text>'
    )

    def marker(kind: str, x: float, y: float) -> str:
        if kind == "square":
            return f'<rect x="{x - 4}" y="{y - 4}" width="8" height="8" fill="#111" stroke="#111"/>'
        if kind == "diamond":
            return (
                f'<polygon points="{x},{y - 5} {x + 5},{y} {x},{y + 5} {x - 5},{y}" '
                f'fill="#fff" stroke="#111" stroke-width="1.5"/>'
            )
        if kind == "circle-open":
            return f'<circle cx="{x}" cy="{y}" r="4.5" fill="#fff" stroke="#111" stroke-width="1.5"/>'
        return f'<circle cx="{x}" cy="{y}" r="4" fill="#111"/>'

    for _name, style, mark, vals in series:
        pts = " ".join(f"{sx(years[i])},{sy(vals[i])}" for i in range(len(years)))
        dashattr = f' stroke-dasharray="{dash[style]}"' if dash[style] else ""
        parts.append(
            f'<polyline points="{pts}" fill="none" stroke="#111" stroke-width="2"{dashattr}/>'
        )
        for i, v in enumerate(vals):
            parts.append(marker(mark, sx(years[i]), sy(v)))

    # legend
    ly = H - 55
    legend_items = [
        ("Jacksonville, Florida", "solid", "square"),
        ("Albuquerque, New Mexico", "dashed", "diamond"),
        ("Boise, Idaho", "dotted", "circle-open"),
        ("New York City, New York", "solid", "circle"),
    ]
    x = pad_l
    for name, style, mark in legend_items:
        dashattr = f' stroke-dasharray="{dash[style]}"' if dash[style] else ""
        parts.append(
            f'<line x1="{x}" y1="{ly}" x2="{x + 28}" y2="{ly}" stroke="#111" stroke-width="2"{dashattr}/>'
        )
        parts.append(marker(mark, x + 14, ly))
        parts.append(
            f'<text x="{x + 36}" y="{ly + 4}" font-family="{FONT}" font-size="10">{name}</text>'
        )
        x += 145 if "New York" not in name else 160
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def eng2_q11_form4720() -> str:
    """Grouped bar: Form 4720s filed vs penalties by taxable activity, 2005.

    Values chosen so answer A holds: SD+TE penalties (~45%) < undistributed income (~55%).
    """
    W, H = 640, 460
    pad_l, pad_r, pad_t, pad_b = 70, 30, 80, 120
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    y_max = 90
    cats = ["percentage of forms", "percentage of penalties"]
    # light gray, medium gray, black — matches source legend order
    series = [
        ("self-dealing", "#d1d5db", [9, 40]),
        ("taxable expenditures", "#6b7280", [6, 5]),
        ("undistributed income", "#111", [85, 55]),
    ]
    parts = [
        f'<text x="{W / 2}" y="22" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700">Percentages of Form 4720s Filed and Total Penalties Assessed on</text>',
        f'<text x="{W / 2}" y="42" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700">Private Foundations, by Taxable Activity, 2005</text>',
        f'<text x="16" y="{(pad_t + H - pad_b) / 2}" text-anchor="middle" font-family="{FONT}" font-size="12" transform="rotate(-90 16 {(pad_t + H - pad_b) / 2})">percentage</text>',
    ]
    for v in range(0, 91, 10):
        y = pad_t + plot_h - (v / y_max) * plot_h
        parts.append(
            f'<line x1="{pad_l}" y1="{y}" x2="{W - pad_r}" y2="{y}" stroke="#e5e7eb"/>'
            f'<text x="{pad_l - 8}" y="{y + 4}" text-anchor="end" font-family="{FONT}" font-size="11">{v}</text>'
        )
    parts.append(
        f'<rect x="{pad_l}" y="{pad_t}" width="{plot_w}" height="{plot_h}" fill="none" stroke="#111"/>'
    )
    gw = plot_w / 2
    bw = gw * 0.18
    for gi, cat in enumerate(cats):
        gx = pad_l + gi * gw
        for si, (_name, color, vals) in enumerate(series):
            val = vals[gi]
            h = (val / y_max) * plot_h
            x = gx + gw * 0.22 + si * (bw + 8)
            parts.append(
                f'<rect x="{x}" y="{pad_t + plot_h - h}" width="{bw}" height="{h}" fill="{color}" stroke="#111"/>'
            )
        parts.append(
            f'<text x="{gx + gw / 2}" y="{H - pad_b + 24}" text-anchor="middle" font-family="{FONT}" font-size="12">{cat}</text>'
        )
    lx, ly = pad_l + 30, H - 48
    for i, (name, color, _) in enumerate(series):
        x = lx + i * 190
        parts.append(
            f'<rect x="{x}" y="{ly}" width="12" height="12" fill="{color}" stroke="#111"/>'
            f'<text x="{x + 18}" y="{ly + 11}" font-family="{FONT}" font-size="11">{name}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def eng2_q12_mortar() -> str:
    """Grouped bar: Compressive Strength of Mortar Mixtures After Curing."""
    W, H = 620, 440
    pad_l, pad_r, pad_t, pad_b = 80, 30, 60, 110
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    y_max = 30
    mixtures = ["control (0% SSA)", "10% SSA", "20% SSA", "40% SSA"]
    day7 = [22.5, 24.5, 19.0, 13.0]
    day28 = [26.0, 25.5, 21.5, 15.0]
    parts = [
        f'<text x="{W / 2}" y="28" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700">Compressive Strength of Mortar Mixtures After Curing</text>',
        f'<text x="18" y="{(pad_t + H - pad_b) / 2}" text-anchor="middle" font-family="{FONT}" font-size="11" transform="rotate(-90 18 {(pad_t + H - pad_b) / 2})">Compressive strength (megapascals)</text>',
    ]
    for v in range(0, 31, 5):
        y = pad_t + plot_h - (v / y_max) * plot_h
        parts.append(
            f'<line x1="{pad_l}" y1="{y}" x2="{W - pad_r}" y2="{y}" stroke="#e5e7eb"/>'
            f'<text x="{pad_l - 8}" y="{y + 4}" text-anchor="end" font-family="{FONT}" font-size="11">{v}</text>'
        )
    parts.append(
        f'<rect x="{pad_l}" y="{pad_t}" width="{plot_w}" height="{plot_h}" fill="none" stroke="#111"/>'
    )
    gw = plot_w / 4
    bw = gw * 0.28
    for gi, mix in enumerate(mixtures):
        gx = pad_l + gi * gw
        for si, (val, color) in enumerate([(day7[gi], "#d1d5db"), (day28[gi], "#111")]):
            h = (val / y_max) * plot_h
            x = gx + gw * 0.22 + si * (bw + 6)
            parts.append(
                f'<rect x="{x}" y="{pad_t + plot_h - h}" width="{bw}" height="{h}" fill="{color}" stroke="#111"/>'
            )
        parts.append(
            f'<text x="{gx + gw / 2}" y="{H - pad_b + 22}" text-anchor="middle" font-family="{FONT}" font-size="11">{mix}</text>'
        )
    parts.append(
        f'<text x="{W / 2}" y="{H - pad_b + 42}" text-anchor="middle" font-family="{FONT}" font-size="12">Mixture</text>'
    )
    lx = pad_l + 160
    ly = H - 42
    parts.append(
        f'<rect x="{lx}" y="{ly}" width="12" height="12" fill="#d1d5db" stroke="#111"/>'
        f'<text x="{lx + 18}" y="{ly + 11}" font-family="{FONT}" font-size="11">day 7</text>'
        f'<rect x="{lx + 90}" y="{ly}" width="12" height="12" fill="#111" stroke="#111"/>'
        f'<text x="{lx + 108}" y="{ly + 11}" font-family="{FONT}" font-size="11">day 28</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q01_candle() -> str:
    """First-quadrant decreasing line: weight vs time (candle wax)."""
    W, H = 520, 420
    pad_l, pad_r, pad_t, pad_b = 70, 30, 30, 60
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b

    def sx(x: float) -> float:
        return pad_l + (x / 14) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((14 - y) / 14) * plot_h

    parts: list[str] = []
    for i in range(0, 15):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" stroke="#e5e7eb"/>'
            f'<line x1="{pad_l}" y1="{sy(i)}" x2="{pad_l + plot_w}" y2="{sy(i)}" stroke="#e5e7eb"/>'
        )
    for i in range(0, 15, 2):
        parts.append(
            f'<text x="{sx(i)}" y="{pad_t + plot_h + 20}" text-anchor="middle" font-family="{FONT}" font-size="12">{i}</text>'
            f'<text x="{pad_l - 10}" y="{sy(i) + 4}" text-anchor="end" font-family="{FONT}" font-size="12">{i}</text>'
        )
    # y = -0.25x + 13
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{sx(0)}" y1="{sy(13)}" x2="{sx(14)}" y2="{sy(9.5)}" stroke="#111" stroke-width="2.5"/>'
        f'<text x="{pad_l + plot_w / 2}" y="{H - 12}" text-anchor="middle" font-family="{FONT}" font-size="13">Time (hours)</text>'
        f'<text x="16" y="{pad_t + plot_h / 2}" text-anchor="middle" font-family="{FONT}" font-size="13" transform="rotate(-90 16 {pad_t + plot_h / 2})">Weight (ounces)</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q04_xy_table() -> str:
    return table_svg("", ["x", "y"], [["0", "22"], ["1", "23"], ["2", "24"]], [80, 80])


def math1_q21_triangle_fgh() -> str:
    """Right triangle FGH; right angle at F (bottom-right); G 60°; hypotenuse GH=68."""
    W, H = 420, 360
    G = (80, 290)
    F = (300, 290)
    Hpt = (300, 80)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="{G[0]},{G[1]} {F[0]},{F[1]} {Hpt[0]},{Hpt[1]}" fill="none" stroke="#111" stroke-width="2.5"/>
  <rect x="{F[0] - 16}" y="{F[1] - 16}" width="16" height="16" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="{G[0] - 18}" y="{G[1] + 6}" font-family="{FONT}" font-size="16" font-weight="700">G</text>
  <text x="{F[0] + 10}" y="{F[1] + 6}" font-family="{FONT}" font-size="16" font-weight="700">F</text>
  <text x="{Hpt[0] + 10}" y="{Hpt[1] + 8}" font-family="{FONT}" font-size="16" font-weight="700">H</text>
  <text x="{(G[0] + Hpt[0]) / 2 - 18}" y="{(G[1] + Hpt[1]) / 2}" font-family="{FONT}" font-size="15">68</text>
  <path d="M {G[0] + 36},{G[1]} A 36 36 0 0 1 {G[0] + 18},{G[1] - 31}" fill="none" stroke="#111" stroke-width="1.2"/>
  <text x="{G[0] + 42}" y="{G[1] - 14}" font-family="{FONT}" font-size="14">60°</text>
  <text x="{W / 2}" y="340" text-anchor="middle" font-family="{FONT}" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math2_q07_inequality_choices() -> str:
    """Four xy-plane choice graphs A–D for 4x+5y < 9."""
    size = 240
    pad = 28
    span = 20  # -10..10

    def s(v: float) -> float:
        return pad + ((v + 10) / span) * (size - 2 * pad)

    def panel(
        label: str,
        slope: float,
        intercept: float,
        shade_origin_side: bool,
        ox: float,
        oy: float,
    ) -> str:
        # line y = slope*x + intercept
        x1, x2 = -10.0, 10.0
        y1 = slope * x1 + intercept
        y2 = slope * x2 + intercept
        # clip y to plot for polygon corners
        # shade: if shade_origin_side, include (0,0)
        # origin is below the correct line (y < -0.8x+1.8)
        if shade_origin_side:
            # polygon: line endpoints + bottom-left corner region containing origin
            poly = f"{s(x1)},{s(-y1)} {s(x2)},{s(-y2)} {s(10)},{s(10)} {s(-10)},{s(10)}"
            # For positive slope with shade "above/left": use top side
            # Detect via slope sign for A vs C styling from NEEDS_SVG
        else:
            poly = f"{s(x1)},{s(-y1)} {s(x2)},{s(-y2)} {s(10)},{s(-10)} {s(-10)},{s(-10)}"

        # Refine shading using half-plane test at corners
        def on_shade(px: float, py: float) -> bool:
            # line: y - (slope*x + intercept)  ; shade where y ? line
            # origin side means y < slope*x+intercept when slope negative (correct)
            # For general: shade where (py - (slope*px+intercept)) has same sign as (0 - intercept)
            line_at = slope * px + intercept
            origin_side = 0 - intercept  # negative if intercept > 0
            val = py - line_at
            if shade_origin_side:
                return val * origin_side >= 0 or abs(val) < 1e-9
            return val * origin_side < 0

        corners = [(-10, -10), (10, -10), (10, 10), (-10, 10)]
        # Build shade polygon by walking boundary: use line + corners that are shaded
        shaded_corners = [(cx, cy) for cx, cy in corners if on_shade(cx, cy)]
        # Order: start at left line point, then shaded corners clockwise, then right line point
        # Simpler fixed polygons matching NEEDS descriptions:
        if slope < 0 and shade_origin_side:
            # C: shade below/left including origin
            poly = f"{s(x1)},{s(-y1)} {s(x2)},{s(-y2)} {s(10)},{s(10)} {s(-10)},{s(10)}"
        elif slope < 0 and not shade_origin_side:
            # D: shade above/right excluding origin
            poly = f"{s(x1)},{s(-y1)} {s(x2)},{s(-y2)} {s(10)},{s(-10)} {s(-10)},{s(-10)}"
        elif slope > 0 and shade_origin_side:
            # A: positive slope, shade above/left
            poly = f"{s(x1)},{s(-y1)} {s(x2)},{s(-y2)} {s(10)},{s(-10)} {s(-10)},{s(-10)}"
        else:
            # B: positive slope, shade below/right
            poly = f"{s(x1)},{s(-y1)} {s(x2)},{s(-y2)} {s(10)},{s(10)} {s(-10)},{s(10)}"

        grid = []
        for i in range(-10, 11):
            stroke = "#e5e7eb" if i % 2 else "#d1d5db"
            grid.append(
                f'<line x1="{s(i)}" y1="{s(-10)}" x2="{s(i)}" y2="{s(10)}" stroke="{stroke}"/>'
                f'<line x1="{s(-10)}" y1="{s(-i)}" x2="{s(10)}" y2="{s(-i)}" stroke="{stroke}"/>'
            )
        labels = []
        for i in range(-10, 11, 2):
            if i == 0:
                continue
            labels.append(
                f'<text x="{s(i)}" y="{s(0) + 14}" text-anchor="middle" font-family="{FONT}" font-size="9">{i}</text>'
                f'<text x="{s(0) - 10}" y="{s(-i) + 3}" text-anchor="end" font-family="{FONT}" font-size="9">{i}</text>'
            )
        return f'''
  <g transform="translate({ox},{oy})">
    <text x="0" y="14" font-family="{FONT}" font-size="15" font-weight="700">{label}</text>
    <rect x="0" y="22" width="{size}" height="{size}" fill="#fff" stroke="#111"/>
    <g transform="translate(0,22)">
      {"".join(grid)}
      <polygon points="{poly}" fill="#c4c4c4" fill-opacity="0.85"/>
      <line x1="{s(0)}" y1="{s(-10)}" x2="{s(0)}" y2="{s(10)}" stroke="#111" stroke-width="1.5"/>
      <line x1="{s(-10)}" y1="{s(0)}" x2="{s(10)}" y2="{s(0)}" stroke="#111" stroke-width="1.5"/>
      <line x1="{s(x1)}" y1="{s(-y1)}" x2="{s(x2)}" y2="{s(-y2)}" stroke="#111" stroke-width="2" stroke-dasharray="6 4"/>
      {"".join(labels)}
      <text x="{s(0) + 8}" y="{s(0) + 14}" font-family="{FONT}" font-size="10">O</text>
      <text x="{s(10) - 8}" y="{s(0) - 6}" font-family="{FONT}" font-size="11" font-style="italic">x</text>
      <text x="{s(0) + 6}" y="{s(-10) + 12}" font-family="{FONT}" font-size="11" font-style="italic">y</text>
    </g>
  </g>'''

    # A/B: positive slope through (-2.25,0) and (0,1.8) → y = 0.8x + 1.8
    # C/D: y = -0.8x + 1.8  (4x+5y=9)
    panels = [
        panel("A", 0.8, 1.8, True, 10, 0),
        panel("B", 0.8, 1.8, False, 280, 0),
        panel("C", -0.8, 1.8, True, 10, 290),
        panel("D", -0.8, 1.8, False, 280, 290),
    ]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="540" height="580" viewBox="0 0 540 580">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(panels)}
</svg>'''


def math2_q15_scatter() -> str:
    """Scatterplot with line of best fit; axis breaks after 0."""
    W, H = 560, 440
    pad_l, pad_r, pad_t, pad_b = 70, 40, 40, 50
    # leave room for axis break near origin
    break_gap = 28
    plot_w = W - pad_l - pad_r - break_gap
    plot_h = H - pad_t - pad_b - break_gap
    t0, t1 = 230, 270
    d0, d1 = 245, 525

    def sx(t: float) -> float:
        return pad_l + break_gap + ((t - t0) / (t1 - t0)) * plot_w

    def sy(d: float) -> float:
        return pad_t + ((d1 - d) / (d1 - d0)) * plot_h

    # points clustered around d = -65.1 + 2.02t
    points = [
        (232, 402),
        (238, 418),
        (245, 428),
        (250, 442),
        (255, 448),
        (260, 462),
        (265, 470),
        (268, 478),
    ]
    parts: list[str] = []
    # grid every 5 on t, every 35 on d
    for t in range(230, 271, 5):
        parts.append(
            f'<line x1="{sx(t)}" y1="{pad_t}" x2="{sx(t)}" y2="{pad_t + plot_h}" stroke="#e5e7eb"/>'
        )
    for d in range(245, 526, 35):
        parts.append(
            f'<line x1="{pad_l + break_gap}" y1="{sy(d)}" x2="{W - pad_r}" y2="{sy(d)}" stroke="#e5e7eb"/>'
        )
    for t in range(230, 271, 10):
        parts.append(
            f'<text x="{sx(t)}" y="{pad_t + plot_h + break_gap + 18}" text-anchor="middle" font-family="{FONT}" font-size="11">{t}</text>'
        )
    for d in range(245, 526, 35):
        parts.append(
            f'<text x="{pad_l - 8}" y="{sy(d) + 4}" text-anchor="end" font-family="{FONT}" font-size="11">{d}</text>'
        )
    # axes with breaks
    ox = pad_l
    oy = pad_t + plot_h + break_gap
    parts.append(
        f'<line x1="{ox}" y1="{pad_t}" x2="{ox}" y2="{oy - break_gap - 4}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{ox}" y1="{oy}" x2="{W - pad_r}" y2="{oy}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy - 8}" stroke="#111" stroke-width="1.5"/>'
        # axis break marks
        f'<line x1="{ox - 6}" y1="{oy - break_gap + 4}" x2="{ox + 6}" y2="{oy - break_gap - 6}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{ox - 6}" y1="{oy - break_gap + 10}" x2="{ox + 6}" y2="{oy - break_gap}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{ox + break_gap - 8}" y1="{oy - 6}" x2="{ox + break_gap + 2}" y2="{oy + 6}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{ox + break_gap - 4}" y1="{oy - 6}" x2="{ox + break_gap + 6}" y2="{oy + 6}" stroke="#111" stroke-width="1.5"/>'
        f'<text x="{ox - 4}" y="{oy + 16}" text-anchor="end" font-family="{FONT}" font-size="11">0</text>'
        f'<text x="{ox + 10}" y="{oy + 16}" font-family="{FONT}" font-size="11">0</text>'
    )
    # line of best fit through ~(230,400) and ~(270,480)
    parts.append(
        f'<line x1="{sx(230)}" y1="{sy(399.5)}" x2="{sx(270)}" y2="{sy(480.3)}" stroke="#111" stroke-width="2"/>'
    )
    for t, d in points:
        parts.append(f'<circle cx="{sx(t)}" cy="{sy(d)}" r="4.5" fill="#111"/>')
    parts.append(
        f'<text x="{W - pad_r + 8}" y="{oy + 4}" font-family="{FONT}" font-size="14" font-style="italic">t</text>'
        f'<text x="{ox + 6}" y="{pad_t + 4}" font-family="{FONT}" font-size="14" font-style="italic">d</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def main() -> None:
    write("eng1-q10-lakes-ice.svg", eng1_q10_lakes_ice())
    write("eng1-q11-traffic-delay.svg", eng1_q11_traffic_delay())
    write("eng2-q11-form4720.svg", eng2_q11_form4720())
    write("eng2-q12-mortar-strength.svg", eng2_q12_mortar())
    write("math1-q01-candle-weight.svg", math1_q01_candle())
    write("math1-q04-xy-table.svg", math1_q04_xy_table())
    write("math1-q21-triangle-fgh.svg", math1_q21_triangle_fgh())
    write("math2-q07-inequality-choices.svg", math2_q07_inequality_choices())
    write("math2-q15-scatter-td.svg", math2_q15_scatter())
    print("done all purplebook-test-5 figures")


if __name__ == "__main__":
    main()
