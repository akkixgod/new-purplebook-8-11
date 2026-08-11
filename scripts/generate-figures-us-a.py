#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2026 March US-A."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2026-march-us-a/figures")
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
    widths = col_widths or ([180] + [140] * (len(headers) - 1))
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
            f'<text x="{x + widths[i]/2}" y="{y0 + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="12" font-weight="700">{h}</text>'
        )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + row_h * (r + 1)
        x = x0
        for i, cell in enumerate(row):
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i]/2}" y="{y + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="12">{cell}</text>'
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


def inequality_m1q1() -> str:
    # dashed y=3x+12, shade below
    W, H = 420, 400
    pad = 50
    plot = 320

    def sx(x):
        return pad + ((x + 5) / 14) * plot

    def sy(y):
        return pad + ((14 - y) / 14) * plot

    grid = []
    for i in range(-4, 10):
        grid.append(f'<line x1="{sx(i)}" y1="{pad}" x2="{sx(i)}" y2="{pad+plot}" stroke="#e5e7eb"/>')
    for j in range(0, 15):
        grid.append(f'<line x1="{pad}" y1="{sy(j)}" x2="{pad+plot}" y2="{sy(j)}" stroke="#e5e7eb"/>')
    labels = "".join(
        f'<text x="{sx(i)}" y="{pad+plot+18}" text-anchor="middle" font-family="Arial" font-size="12">{i}</text>'
        for i in (-4, 4, 8)
    ) + "".join(
        f'<text x="{pad-8}" y="{sy(j)+4}" text-anchor="end" font-family="Arial" font-size="12">{j}</text>'
        for j in (4, 8, 12)
    )
    # shade polygon below line from x=-4 to x=8
    xs = [-4, -2, 0, 2]
    pts = [(sx(x), sy(3 * x + 12)) for x in xs]
    poly = " ".join(f"{x},{y}" for x, y in pts) + f" {sx(2)},{pad+plot} {sx(-4)},{pad+plot}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <polygon points="{poly}" fill="#d1d5db" fill-opacity="0.7"/>
  <line x1="{sx(0)}" y1="{pad}" x2="{sx(0)}" y2="{pad+plot}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad}" y1="{sy(0)}" x2="{pad+plot}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>
  <line x1="{sx(-4)}" y1="{sy(0)}" x2="{sx(0.5)}" y2="{sy(13.5)}" stroke="#111" stroke-width="2.5" stroke-dasharray="8 5"/>
  {labels}
  <text x="{sx(0)+6}" y="{sy(0)+16}" font-family="Arial" font-size="12">O</text>
  <text x="{pad+plot-8}" y="{sy(0)-8}" font-family="Arial" font-size="14" font-style="italic">x</text>
  <text x="{sx(0)+8}" y="{pad+14}" font-family="Arial" font-size="14" font-style="italic">y</text>
</svg>'''


def similar_triangles() -> str:
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


def line_parabola_m1q4() -> str:
    W, H = 480, 400
    pad = 50
    plot = 320

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
    while x <= -2.0:
        y = 3 - (x + 5) ** 2
        if -5 <= y <= 7:
            pts.append(f"{sx(x):.2f},{sy(y):.2f}")
        x += 0.05
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <line x1="{sx(0)}" y1="{pad}" x2="{sx(0)}" y2="{pad+plot}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad}" y1="{sy(0)}" x2="{pad+plot}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad}" y1="{sy(3)}" x2="{pad+plot}" y2="{sy(3)}" stroke="#111" stroke-width="2"/>
  <path d="M {" L ".join(pts)}" fill="none" stroke="#111" stroke-width="2.5"/>
  <text x="{sx(0)+6}" y="{sy(0)+16}" font-family="Arial" font-size="12">O</text>
</svg>'''


def intersecting_angles() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="320" viewBox="0 0 420 320">
  <rect width="100%" height="100%" fill="#fff"/>
  <line x1="40" y1="220" x2="380" y2="80" stroke="#111" stroke-width="2"/>
  <line x1="60" y1="60" x2="360" y2="240" stroke="#111" stroke-width="2"/>
  <text x="150" y="145" font-family="Arial" font-size="16" font-style="italic">r°</text>
  <text x="250" y="175" font-family="Arial" font-size="16" font-style="italic">s°</text>
  <text x="210" y="300" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def inequality_choices_m1q14() -> str:
    """A–D graphs for y ≤ -1/4 x + 7; correct is solid negative slope, shade below (=C per key)."""

    def panel(lab, slope, shade_below, ox, oy):
        size = 200
        pad = 20

        def sx(x):
            return pad + ((x + 8) / 16) * (size - 2 * pad)

        def sy(y):
            return pad + ((12 - y) / 12) * (size - 2 * pad)

        grid = []
        for i in range(-8, 9, 2):
            grid.append(f'<line x1="{sx(i)}" y1="{pad}" x2="{sx(i)}" y2="{size-pad}" stroke="#eee"/>')
        for j in range(0, 13, 2):
            grid.append(f'<line x1="{pad}" y1="{sy(j)}" x2="{size-pad}" y2="{sy(j)}" stroke="#eee"/>')
        # shade
        y_left = slope * (-8) + 7
        y_right = slope * 8 + 7
        if shade_below:
            poly = f"{sx(-8)},{sy(y_left)} {sx(8)},{sy(y_right)} {sx(8)},{sy(0)} {sx(-8)},{sy(0)}"
        else:
            poly = f"{sx(-8)},{sy(y_left)} {sx(8)},{sy(y_right)} {sx(8)},{sy(12)} {sx(-8)},{sy(12)}"
        return f'''
  <g transform="translate({ox},{oy})">
    <text x="0" y="14" font-family="Arial" font-size="15" font-weight="700">{lab})</text>
    <rect x="0" y="20" width="{size}" height="{size}" fill="#fff" stroke="#ddd"/>
    <g transform="translate(0,20)">
      {"".join(grid)}
      <polygon points="{poly}" fill="#d1d5db" fill-opacity="0.75"/>
      <line x1="{sx(0)}" y1="{pad}" x2="{sx(0)}" y2="{size-pad}" stroke="#111"/>
      <line x1="{pad}" y1="{sy(0)}" x2="{size-pad}" y2="{sy(0)}" stroke="#111"/>
      <line x1="{sx(-8)}" y1="{sy(y_left)}" x2="{sx(8)}" y2="{sy(y_right)}" stroke="#111" stroke-width="2"/>
    </g>
  </g>'''

    panels = [
        panel("A", 0.25, True, 10, 10),
        panel("B", 0.25, False, 240, 10),
        panel("C", -0.25, True, 10, 250),  # key C
        panel("D", -0.25, False, 240, 250),
    ]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="460" height="480" viewBox="0 0 460 480">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(panels)}
</svg>'''


def q_tables_m1q15() -> str:
    opts = [
        ("A", ["14", "28", "56"]),
        ("B", ["1/14", "28", "56"]),
        ("C", ["1/14", "2", "56"]),
        ("D", ["-56", "0", "56"]),
    ]
    panels = []
    for idx, (lab, vals) in enumerate(opts):
        ox = 20 + (idx % 2) * 280
        oy = 20 + (idx // 2) * 130
        cells = []
        for r, row in enumerate([["x", "-1", "0", "1"], ["q(x)"] + vals]):
            for c, val in enumerate(row):
                x, y = ox + c * 55, oy + 24 + r * 34
                fill = "#f3f4f6" if r == 0 or c == 0 else "#fff"
                cells.append(
                    f'<rect x="{x}" y="{y}" width="55" height="34" fill="{fill}" stroke="#111"/>'
                    f'<text x="{x+27}" y="{y+23}" text-anchor="middle" font-family="Arial" font-size="13">{val}</text>'
                )
        panels.append(f'<text x="{ox}" y="{oy+16}" font-family="Arial" font-size="15" font-weight="700">{lab})</text>' + "".join(cells))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="580" height="280" viewBox="0 0 580 280">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(panels)}
</svg>'''


def parabola_line_m1q19() -> str:
    W, H = 420, 400
    pad = 50
    plot = 320

    def sx(x):
        return pad + (x / 10) * plot

    def sy(y):
        return pad + ((10 - y) / 10) * plot

    grid = []
    for i in range(0, 11):
        grid.append(f'<line x1="{sx(i)}" y1="{pad}" x2="{sx(i)}" y2="{pad+plot}" stroke="#e5e7eb"/>')
        grid.append(f'<line x1="{pad}" y1="{sy(i)}" x2="{pad+plot}" y2="{sy(i)}" stroke="#e5e7eb"/>')
        if i % 2 == 0:
            grid.append(f'<text x="{sx(i)}" y="{pad+plot+16}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>')
            grid.append(f'<text x="{pad-8}" y="{sy(i)+4}" text-anchor="end" font-family="Arial" font-size="11">{i}</text>')
    pts = []
    x = 1.5
    while x <= 6.5:
        y = (x - 4) ** 2 + 3
        pts.append(f"{sx(x):.2f},{sy(y):.2f}")
        x += 0.05
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <line x1="{sx(0)}" y1="{pad}" x2="{sx(0)}" y2="{pad+plot}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad}" y1="{sy(0)}" x2="{pad+plot}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>
  <path d="M {" L ".join(pts)}" fill="none" stroke="#111" stroke-width="2.5"/>
  <line x1="{sx(6)}" y1="{sy(7)}" x2="{sx(9)}" y2="{sy(1)}" stroke="#111" stroke-width="2.5"/>
  <text x="{sx(0)+6}" y="{sy(0)+16}" font-family="Arial" font-size="12">O</text>
</svg>'''


def bar_programs() -> str:
    W, H = 520, 380
    pad_l, pad_r, pad_t, pad_b = 55, 30, 30, 80
    plot_w, plot_h = W - pad_l - pad_r, H - pad_t - pad_b
    cats = [("volleyball", 30), ("hockey", 40), ("basketball", 57), ("soccer", 43)]
    bw = plot_w / len(cats) * 0.55
    bars, labels = [], []
    for i, (name, v) in enumerate(cats):
        h = (v / 60) * plot_h
        x = pad_l + i * (plot_w / len(cats)) + (plot_w / len(cats) - bw) / 2
        y = pad_t + plot_h - h
        bars.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" fill="#e5e7eb" stroke="#111"/>')
        labels.append(
            f'<text x="{x+bw/2}" y="{pad_t+plot_h+28}" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-20 {x+bw/2} {pad_t+plot_h+28})">{name}</text>'
        )
    ygrid = "".join(
        f'<line x1="{pad_l}" y1="{pad_t + plot_h - (v/60)*plot_h}" x2="{pad_l+plot_w}" y2="{pad_t + plot_h - (v/60)*plot_h}" stroke="#e5e7eb"/>'
        f'<text x="{pad_l-8}" y="{pad_t + plot_h - (v/60)*plot_h + 4}" text-anchor="end" font-family="Arial" font-size="11">{v}</text>'
        for v in range(0, 61, 10)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {ygrid}
  {"".join(bars)}
  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t+plot_h}" stroke="#111"/>
  <line x1="{pad_l}" y1="{pad_t+plot_h}" x2="{pad_l+plot_w}" y2="{pad_t+plot_h}" stroke="#111"/>
  {"".join(labels)}
  <text x="16" y="{pad_t+plot_h/2}" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-90 16 {pad_t+plot_h/2})">Number of students</text>
  <text x="{pad_l+plot_w/2}" y="{H-12}" text-anchor="middle" font-family="Arial" font-size="13">Program</text>
</svg>'''


def triangle_abc() -> str:
    A, B, C = (300, 70), (300, 280), (80, 280)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="360" viewBox="0 0 420 360">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="none" stroke="#111" stroke-width="2"/>
  <rect x="{B[0]-14}" y="{B[1]-14}" width="14" height="14" fill="none" stroke="#111"/>
  <text x="{A[0]+10}" y="{A[1]+6}" font-family="Arial" font-size="16" font-weight="700">A</text>
  <text x="{B[0]+10}" y="{B[1]+22}" font-family="Arial" font-size="16" font-weight="700">B</text>
  <text x="{C[0]-18}" y="{C[1]+22}" font-family="Arial" font-size="16" font-weight="700">C</text>
  <text x="{(A[0]+B[0])/2 + 12}" y="{(A[1]+B[1])/2 + 6}" font-family="Arial" font-size="15">22</text>
  <text x="{(A[0]+C[0])/2 - 18}" y="{(A[1]+C[1])/2}" font-family="Arial" font-size="15">43</text>
  <text x="210" y="340" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def pyramid() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="340" viewBox="0 0 420 340">
  <rect width="100%" height="100%" fill="#fff"/>
  <!-- base parallelogram -->
  <path d="M 80,240 L 260,240 L 320,190 L 140,190 Z" fill="none" stroke="#111" stroke-width="2"/>
  <line x1="140" y1="190" x2="200" y2="60" stroke="#111" stroke-width="2"/>
  <line x1="320" y1="190" x2="200" y2="60" stroke="#111" stroke-width="2"/>
  <line x1="80" y1="240" x2="200" y2="60" stroke="#111" stroke-width="2"/>
  <line x1="260" y1="240" x2="200" y2="60" stroke="#111" stroke-width="2"/>
  <!-- height dashed -->
  <line x1="200" y1="60" x2="200" y2="215" stroke="#111" stroke-width="1.5" stroke-dasharray="5 4"/>
  <rect x="200" y="201" width="12" height="12" fill="none" stroke="#111"/>
  <text x="165" y="265" font-family="Arial" font-size="16" font-style="italic">l</text>
  <text x="295" y="225" font-family="Arial" font-size="16" font-style="italic">w</text>
  <text x="210" y="140" font-family="Arial" font-size="16" font-style="italic">h</text>
  <text x="210" y="320" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def scatter_m2q14() -> str:
    W, H = 440, 400
    pad = 50
    plot = 320
    xmax = ymax = 15.0

    def sx(x):
        return pad + (x / xmax) * plot

    def sy(y):
        return pad + ((ymax - y) / ymax) * plot

    points = [(1, 13), (3, 11), (4, 9), (6, 12), (7, 8), (9, 5), (11, 6), (13, 2)]
    grid = []
    for i in range(0, 15, 2):
        grid.append(f'<line x1="{sx(i)}" y1="{pad}" x2="{sx(i)}" y2="{pad+plot}" stroke="#e5e7eb"/>')
        grid.append(f'<line x1="{pad}" y1="{sy(i)}" x2="{pad+plot}" y2="{sy(i)}" stroke="#e5e7eb"/>')
        grid.append(f'<text x="{sx(i)}" y="{pad+plot+16}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>')
        grid.append(f'<text x="{pad-8}" y="{sy(i)+4}" text-anchor="end" font-family="Arial" font-size="11">{i}</text>')
    dots = "".join(f'<circle cx="{sx(x)}" cy="{sy(y)}" r="4.5" fill="#111"/>' for x, y in points)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <line x1="{pad}" y1="{pad}" x2="{pad}" y2="{pad+plot}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad}" y1="{pad+plot}" x2="{pad+plot}" y2="{pad+plot}" stroke="#111" stroke-width="1.5"/>
  <line x1="{sx(0)}" y1="{sy(12.4)}" x2="{sx(14)}" y2="{sy(2.6)}" stroke="#111" stroke-width="2"/>
  {dots}
  <text x="{sx(0)+6}" y="{sy(0)+16}" font-family="Arial" font-size="12">O</text>
</svg>'''


def inequality_choices_m2q19() -> str:
    def panel(lab, slope, intercept, shade_below, ox):
        size = 180
        pad = 18

        def s(v):
            return pad + ((v + 10) / 20) * (size - 2 * pad)

        x1, x2 = -10.0, 10.0
        y1, y2 = slope * x1 + intercept, slope * x2 + intercept
        if shade_below:
            poly = f"{s(x1)},{s(-y1)} {s(x2)},{s(-y2)} {s(10)},{s(10)} {s(-10)},{s(10)}"
        else:
            poly = f"{s(x1)},{s(-y1)} {s(x2)},{s(-y2)} {s(10)},{s(-10)} {s(-10)},{s(-10)}"
        return f'''
  <g transform="translate({ox},30)">
    <text x="0" y="-8" font-family="Arial" font-size="15" font-weight="700">{lab})</text>
    <rect x="0" y="0" width="{size}" height="{size}" fill="#fff" stroke="#ddd"/>
    <line x1="{s(0)}" y1="{s(-10)}" x2="{s(0)}" y2="{s(10)}" stroke="#111"/>
    <line x1="{s(-10)}" y1="{s(0)}" x2="{s(10)}" y2="{s(0)}" stroke="#111"/>
    <polygon points="{poly}" fill="#d1d5db" fill-opacity="0.7"/>
    <line x1="{s(x1)}" y1="{s(-y1)}" x2="{s(x2)}" y2="{s(-y2)}" stroke="#111" stroke-width="2" stroke-dasharray="6 4"/>
  </g>'''

    # 4x+5y=9 → y=-0.8x+1.8; key D typically shade excluding origin for >
    panels = [
        panel("A", 0.8, 1.8, False, 20),
        panel("B", 0.8, 1.8, True, 220),
        panel("C", -0.8, 1.8, True, 420),
        panel("D", -0.8, 1.8, False, 620),
    ]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="820" height="240" viewBox="0 0 820 240">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(panels)}
</svg>'''


def main() -> None:
    write(
        "eng1-q14-corals.svg",
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
        "eng2-q07-biking.svg",
        table_svg(
            "Percentage of City's Commuters Regularly Biking to Work in 2016",
            ["City", "% of commuters"],
            [
                ["Albuquerque, New Mexico", "1.6"],
                ["Berkeley, California", "9.0"],
                ["Washington, DC", "4.6"],
                ["Phoenix, Arizona", "0.6"],
            ],
            [240, 140],
        ),
    )
    write(
        "eng2-q14-prices.svg",
        table_svg(
            "Average Paperback Prices, 2016–19",
            ["Genre", "2016", "2017", "2018", "2019"],
            [
                ["Young adult", "$25.49", "$18.40", "$18.02", "$18.40"],
                ["Mathematics", "$97.31", "$78.54", "$106.69", "$76.99"],
                ["Comics and graphic novels", "$18.60", "$18.49", "$19.12", "$20.60"],
                ["Reference", "$156.03", "$189.53", "$186.25", "$148.88"],
            ],
            [220, 90, 90, 90, 90],
        ),
    )
    write(
        "eng2-q15-crabs.svg",
        table_svg(
            "Hermit Crab Reactions to a Shell on a Beach",
            ["Level of shell vibration", "Percentage of crabs that tried to flip the shell over"],
            [
                ["None", "70%"],
                ["Gentle vibration", "19%"],
                ["Strong vibration", "0%"],
            ],
            [220, 360],
        ),
    )
    write("math1-q01-inequality.svg", inequality_m1q1())
    write("math1-q02-triangles.svg", similar_triangles())
    write("math1-q04-line-parabola.svg", line_parabola_m1q4())
    write("math1-q09-angles.svg", intersecting_angles())
    write("math1-q14-choices.svg", inequality_choices_m1q14())
    write("math1-q15-tables.svg", q_tables_m1q15())
    write("math1-q19-parabola-line.svg", parabola_line_m1q19())
    write("math1-q21-bars.svg", bar_programs())
    write(
        "math2-q01-entrees.svg",
        table_svg(
            "",
            ["Type of entree", "Number of people"],
            [
                ["Beef", "20"],
                ["Chicken", "19"],
                ["Fish", "2"],
                ["Vegetarian", "9"],
                ["Total", "50"],
            ],
            [200, 180],
        ),
    )
    write("math2-q06-triangle.svg", triangle_abc())
    write("math2-q10-pyramid.svg", pyramid())
    write("math2-q14-scatter.svg", scatter_m2q14())
    write("math2-q19-choices.svg", inequality_choices_m2q19())


if __name__ == "__main__":
    main()
