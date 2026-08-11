#!/usr/bin/env python3
"""Generate Math Module 1 figures for purplebook-test-9."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/purplebook-test-9/figures")
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def q08_graphs() -> str:
    """Four parabola graphs; A has roots at -5 and 7."""
    W, H = 320, 880
    panel_h = 200
    pad = 16

    def panel(label: str, roots: tuple[float, float], y0: float) -> str:
        # plot box
        bx, by, bw, bh = 48, y0 + 8, 240, 170
        ox = bx + bw / 2
        oy = by + bh / 2
        scale = 10  # px per unit; visible ~±12

        def sx(x: float) -> float:
            return ox + x * scale

        def sy(y: float) -> float:
            return oy - y * scale

        # grid
        grid = []
        for i in range(-10, 11):
            x = sx(i)
            y = sy(i)
            grid.append(
                f'<line x1="{x:.1f}" y1="{by}" x2="{x:.1f}" y2="{by+bh}" stroke="#e5e7eb" stroke-width="1"/>'
            )
            grid.append(
                f'<line x1="{bx}" y1="{y:.1f}" x2="{bx+bw}" y2="{y:.1f}" stroke="#e5e7eb" stroke-width="1"/>'
            )
        axes = (
            f'<line x1="{bx}" y1="{oy:.1f}" x2="{bx+bw}" y2="{oy:.1f}" stroke="#111" stroke-width="1.5"/>'
            f'<line x1="{ox:.1f}" y1="{by}" x2="{ox:.1f}" y2="{by+bh}" stroke="#111" stroke-width="1.5"/>'
        )
        r1, r2 = roots
        # upward parabola through roots: y = 0.08(x-r1)(x-r2)
        pts = []
        for i in range(0, 49):
            x = -11 + 22 * i / 48
            y = 0.08 * (x - r1) * (x - r2)
            if abs(y) > 9:
                continue
            pts.append(f"{sx(x):.1f},{sy(y):.1f}")
        curve = f'<polyline points="{" ".join(pts)}" fill="none" stroke="#111" stroke-width="2"/>'
        return f'''
  <g>
    <circle cx="28" cy="{y0 + panel_h/2:.0f}" r="12" fill="none" stroke="#111" stroke-width="1.5"/>
    <text x="28" y="{y0 + panel_h/2 + 5:.0f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">{label}</text>
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#fff" stroke="#d1d5db"/>
    {"".join(grid)}
    {axes}
    {curve}
  </g>'''

    panels = "".join(
        [
            panel("A", (-5, 7), 10),
            panel("B", (-7, 5), 220),
            panel("C", (-7, -5), 430),
            panel("D", (5, 7), 640),
        ]
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {panels}
</svg>'''


def q11_histogram() -> str:
    """Salmon weight histogram; frequencies sum to 14."""
    # bins: [10,15)=3, [15,20)=5, [20,25)=2, [25,30)=2, [30,35)=2
    freqs = [3, 5, 2, 2, 2]
    edges = [10, 15, 20, 25, 30, 35]
    W, H = 420, 340
    pl, pr, pt, pb = 70, 30, 30, 60
    pw, ph = W - pl - pr, H - pt - pb
    ymax = 6

    def sx(x: float) -> float:
        return pl + (x - 10) / 25 * pw

    def sy(y: float) -> float:
        return pt + (ymax - y) / ymax * ph

    bars = []
    for i, f in enumerate(freqs):
        x0, x1 = edges[i], edges[i + 1]
        bars.append(
            f'<rect x="{sx(x0):.1f}" y="{sy(f):.1f}" width="{sx(x1)-sx(x0):.1f}" height="{sy(0)-sy(f):.1f}" fill="#fff" stroke="#111" stroke-width="1.5"/>'
        )
    yticks = []
    for y in range(0, 7):
        yticks.append(
            f'<line x1="{pl-5}" y1="{sy(y):.1f}" x2="{pl}" y2="{sy(y):.1f}" stroke="#111"/>'
            f'<text x="{pl-10}" y="{sy(y)+4:.1f}" text-anchor="end" font-family="Georgia, serif" font-size="12">{y}</text>'
            f'<line x1="{pl}" y1="{sy(y):.1f}" x2="{pl+pw}" y2="{sy(y):.1f}" stroke="#e5e7eb"/>'
        )
    xticks = []
    for x in edges:
        xticks.append(
            f'<line x1="{sx(x):.1f}" y1="{pt+ph}" x2="{sx(x):.1f}" y2="{pt+ph+5}" stroke="#111"/>'
            f'<text x="{sx(x):.1f}" y="{pt+ph+22}" text-anchor="middle" font-family="Georgia, serif" font-size="12">{x}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(yticks)}
  {"".join(bars)}
  <line x1="{pl}" y1="{pt}" x2="{pl}" y2="{pt+ph}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pl}" y1="{pt+ph}" x2="{pl+pw}" y2="{pt+ph}" stroke="#111" stroke-width="1.5"/>
  {"".join(xticks)}
  <text x="18" y="{pt+ph/2}" text-anchor="middle" transform="rotate(-90 18 {pt+ph/2})" font-family="Georgia, serif" font-size="13">Number of salmon</text>
  <text x="{pl+pw/2}" y="{H-12}" text-anchor="middle" font-family="Georgia, serif" font-size="13">Weight (pounds)</text>
</svg>'''


def q15_tables() -> str:
    """Four choice tables for inequality solutions."""
    tables = {
        "A": [("-8", "14"), ("-9", "35"), ("-11", "-3")],
        "B": [("-8", "19"), ("-9", "22"), ("-11", "-3")],
        "C": [("-8", "18"), ("-9", "25"), ("-11", "-26")],
        "D": [("-8", "18"), ("-9", "22"), ("-11", "26")],
    }
    tw, th = 120, 36
    parts = []
    for i, (lab, rows) in enumerate(tables.items()):
        y0 = 20 + i * 170
        parts.append(
            f'<circle cx="28" cy="{y0 + 70}" r="12" fill="none" stroke="#111" stroke-width="1.5"/>'
            f'<text x="28" y="{y0 + 75}" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">{lab}</text>'
        )
        # header
        x0 = 55
        for j, h in enumerate(["x", "y"]):
            parts.append(
                f'<rect x="{x0 + j*tw}" y="{y0}" width="{tw}" height="{th}" fill="#fff" stroke="#111"/>'
                f'<text x="{x0 + j*tw + tw/2}" y="{y0 + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-style="italic">{h}</text>'
            )
        for r, (xv, yv) in enumerate(rows):
            yy = y0 + th * (r + 1)
            for j, val in enumerate([xv, yv]):
                parts.append(
                    f'<rect x="{x0 + j*tw}" y="{yy}" width="{tw}" height="{th}" fill="#fff" stroke="#111"/>'
                    f'<text x="{x0 + j*tw + tw/2}" y="{yy + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="14">{val}</text>'
                )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="320" height="720" viewBox="0 0 320 720">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def q21_triangle() -> str:
    """Right triangle ABC, right angle at B, hypotenuse AC=32."""
    # A top, B bottom-left with square, C bottom-right; AC labeled 32
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="280" viewBox="0 0 360 280">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="80,220 80,60 300,220" fill="none" stroke="#111" stroke-width="2"/>
  <rect x="80" y="200" width="20" height="20" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="68" y="55" text-anchor="middle" font-family="Georgia, serif" font-size="16" font-style="italic">A</text>
  <text x="68" y="240" text-anchor="middle" font-family="Georgia, serif" font-size="16" font-style="italic">B</text>
  <text x="318" y="240" text-anchor="middle" font-family="Georgia, serif" font-size="16" font-style="italic">C</text>
  <text x="200" y="130" text-anchor="middle" font-family="Georgia, serif" font-size="15">32</text>
  <text x="180" y="265" text-anchor="middle" font-family="Georgia, serif" font-size="12">Note: Figure not drawn to scale.</text>
</svg>'''


if __name__ == "__main__":
    write("math1-q08-polynomial-graphs.svg", q08_graphs())
    write("math1-q11-salmon-histogram.svg", q11_histogram())
    write("math1-q15-inequality-tables.svg", q15_tables())
    write("math1-q21-triangle-abc.svg", q21_triangle())
