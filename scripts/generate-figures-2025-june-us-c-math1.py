#!/usr/bin/env python3
"""Generate clean SVG figures for 2025 June US-C Math Module 1."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-june-us-c/figures")
OUT.mkdir(parents=True, exist_ok=True)
FONT = "Georgia, serif"
ARIAL = "Arial, sans-serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path.name)


def esc(t: object) -> str:
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def math1_q05_triangle() -> None:
    """Right triangle: vertical leg 9, horizontal leg 12, hypotenuse r; right angle bottom-left."""
    bl, br, tl = (90, 260), (360, 260), (90, 80)
    write(
        "math1-q05-right-triangle.svg",
        f'''<svg xmlns="http://www.w3.org/2000/svg" width="440" height="320" viewBox="0 0 440 320">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="{bl[0]},{bl[1]} {br[0]},{br[1]} {tl[0]},{tl[1]}" fill="none" stroke="#111" stroke-width="2.2"/>
  <rect x="{bl[0]}" y="{bl[1] - 18}" width="18" height="18" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="{bl[0] - 22}" y="{(bl[1] + tl[1]) / 2 + 6}" text-anchor="middle" font-family="{FONT}" font-size="20">9</text>
  <text x="{(bl[0] + br[0]) / 2}" y="{bl[1] + 32}" text-anchor="middle" font-family="{FONT}" font-size="20">12</text>
  <text x="{(br[0] + tl[0]) / 2 + 18}" y="{(br[1] + tl[1]) / 2}" text-anchor="middle" font-family="{FONT}" font-size="22" font-style="italic">r</text>
  <text x="220" y="305" text-anchor="middle" font-family="{ARIAL}" font-size="13">Note: Figure not drawn to scale.</text>
</svg>''',
    )


def math1_q09_parallel() -> None:
    """Parallel lines l (top) and k (bottom); transversal t; angles x° (upper obtuse) and y° (lower acute)."""
    # Horizontal parallels
    y_l, y_k = 90, 220
    # Transversal sloping down left→right
    # Upper intersection ~ (180, 90), lower ~ (280, 220)
    write(
        "math1-q09-parallel-lines.svg",
        f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="320" viewBox="0 0 480 320">
  <rect width="100%" height="100%" fill="#fff"/>
  <!-- parallel lines -->
  <line x1="40" y1="{y_l}" x2="420" y2="{y_l}" stroke="#111" stroke-width="2.2"/>
  <line x1="40" y1="{y_k}" x2="420" y2="{y_k}" stroke="#111" stroke-width="2.2"/>
  <!-- transversal -->
  <line x1="80" y1="40" x2="360" y2="270" stroke="#111" stroke-width="2.2"/>
  <!-- line labels -->
  <text x="430" y="{y_l + 5}" font-family="{FONT}" font-size="18" font-style="italic">ℓ</text>
  <text x="430" y="{y_k + 5}" font-family="{FONT}" font-size="18" font-style="italic">k</text>
  <text x="368" y="268" font-family="{FONT}" font-size="18" font-style="italic">t</text>
  <!-- angle x at upper intersection, top-left (obtuse exterior-ish) -->
  <path d="M 155,90 A 28,28 0 0,0 168,68" fill="none" stroke="#111" stroke-width="1.4"/>
  <text x="128" y="72" font-family="{FONT}" font-size="16" font-style="italic">x°</text>
  <!-- angle y at lower intersection, bottom-right (acute) -->
  <path d="M 295,220 A 24,24 0 0,0 312,238" fill="none" stroke="#111" stroke-width="1.4"/>
  <text x="318" y="248" font-family="{FONT}" font-size="16" font-style="italic">y°</text>
  <text x="240" y="305" text-anchor="middle" font-family="{ARIAL}" font-size="13">Note: Figure not drawn to scale.</text>
</svg>''',
    )


def math1_q12_inequality() -> None:
    """Dashed line y=3x+8 through (0,8),(1,11); shade below/right (y < 3x+8)."""
    W, H = 480, 420
    pad = 40
    plot = 340
    xmin, xmax = -4.0, 8.0
    ymin, ymax = -2.0, 14.0

    def sx(x: float) -> float:
        return pad + ((x - xmin) / (xmax - xmin)) * plot

    def sy(y: float) -> float:
        return pad + ((ymax - y) / (ymax - ymin)) * plot

    def f(x: float) -> float:
        return 3 * x + 8

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for i in range(int(xmin), int(xmax) + 1):
        parts.append(
            f'<line x1="{sx(i):.1f}" y1="{pad}" x2="{sx(i):.1f}" y2="{pad + plot}" stroke="#eee"/>'
        )
    for j in range(int(ymin), int(ymax) + 1):
        parts.append(
            f'<line x1="{pad}" y1="{sy(j):.1f}" x2="{pad + plot}" y2="{sy(j):.1f}" stroke="#eee"/>'
        )

    # Shade y < 3x+8 within plot: polygon along line then bottom-right corner
    xs = [xmin + i * (xmax - xmin) / 40 for i in range(41)]
    shade_pts: list[str] = []
    for x in xs:
        y = f(x)
        yy = max(ymin, min(ymax, y))
        shade_pts.append(f"{sx(x):.1f},{sy(yy):.1f}")
    # close via bottom-right, bottom-left of plot clipped to below line
    shade_pts.append(f"{sx(xmax):.1f},{sy(ymin):.1f}")
    shade_pts.append(f"{sx(xmin):.1f},{sy(ymin):.1f}")
    # also need left edge up to line at xmin
    y_left = max(ymin, min(ymax, f(xmin)))
    shade_pts.append(f"{sx(xmin):.1f},{sy(y_left):.1f}")
    parts.append(
        f'<polygon points="{" ".join(shade_pts)}" fill="#d1d5db" fill-opacity="0.55" stroke="none"/>'
    )

    parts.append(
        f'<line x1="{sx(0)}" y1="{pad}" x2="{sx(0)}" y2="{pad + plot}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{pad}" y1="{sy(0)}" x2="{pad + plot}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
    )

    # dashed boundary
    x0, x1 = xmin, xmax
    y0, y1 = f(x0), f(x1)
    # clip to plot
    parts.append(
        f'<line x1="{sx(x0):.1f}" y1="{sy(y0):.1f}" x2="{sx(x1):.1f}" y2="{sy(y1):.1f}" '
        f'stroke="#111" stroke-width="2.2" stroke-dasharray="7 5"/>'
    )

    for i in range(-4, 9, 4):
        if i == 0:
            continue
        parts.append(
            f'<text x="{sx(i):.1f}" y="{sy(0) + 16}" text-anchor="middle" font-family="{ARIAL}" font-size="12">{i}</text>'
        )
    for j in range(0, 13, 4):
        if j == 0:
            continue
        parts.append(
            f'<text x="{sx(0) - 8}" y="{sy(j) + 4:.1f}" text-anchor="end" font-family="{ARIAL}" font-size="12">{j}</text>'
        )
    parts.append(
        f'<text x="{sx(0) + 6}" y="{sy(0) + 16}" font-family="{ARIAL}" font-size="12">O</text>'
    )
    parts.append(
        f'<text x="{pad + plot - 4}" y="{sy(0) - 8}" text-anchor="end" font-family="{ARIAL}" font-size="14" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 8}" y="{pad + 14}" font-family="{ARIAL}" font-size="14" font-style="italic">y</text>'
    )
    parts.append("</svg>")
    write("math1-q12-inequality.svg", "\n".join(parts))


def math1_q14_scatter() -> None:
    """Scatterplot of 11 points, axes 0–10."""
    W, H = 460, 440
    pad = 48
    plot = 340
    xmin, xmax = 0.0, 10.0
    ymin, ymax = 0.0, 10.0
    pts = [
        (0.0, 0.0),
        (0.3, 0.7),
        (1.2, 0.5),
        (1.9, 1.9),
        (2.8, 2.9),
        (3.7, 3.8),
        (4.2, 4.3),
        (4.8, 4.5),
        (6.1, 6.5),
        (7.4, 7.1),
        (9.2, 9.6),
    ]

    def sx(x: float) -> float:
        return pad + ((x - xmin) / (xmax - xmin)) * plot

    def sy(y: float) -> float:
        return pad + ((ymax - y) / (ymax - ymin)) * plot

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for i in range(0, 11):
        parts.append(
            f'<line x1="{sx(i):.1f}" y1="{pad}" x2="{sx(i):.1f}" y2="{pad + plot}" stroke="#eee"/>'
        )
        parts.append(
            f'<line x1="{pad}" y1="{sy(i):.1f}" x2="{pad + plot}" y2="{sy(i):.1f}" stroke="#eee"/>'
        )
    parts.append(
        f'<line x1="{sx(0)}" y1="{pad}" x2="{sx(0)}" y2="{pad + plot}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{pad}" y1="{sy(0)}" x2="{pad + plot}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
    )
    for i in range(0, 11, 2):
        parts.append(
            f'<text x="{sx(i):.1f}" y="{sy(0) + 18}" text-anchor="middle" font-family="{ARIAL}" font-size="12">{i}</text>'
        )
        parts.append(
            f'<text x="{sx(0) - 10}" y="{sy(i) + 4:.1f}" text-anchor="end" font-family="{ARIAL}" font-size="12">{i}</text>'
        )
    for x, y in pts:
        parts.append(
            f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="5" fill="#111"/>'
        )
    parts.append(
        f'<text x="{pad + plot - 4}" y="{sy(0) - 8}" text-anchor="end" font-family="{ARIAL}" font-size="14" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 10}" y="{pad + 14}" font-family="{ARIAL}" font-size="14" font-style="italic">y</text>'
    )
    parts.append("</svg>")
    write("math1-q14-scatter.svg", "\n".join(parts))


def math1_q22_table() -> None:
    headers = ["x", "g(x)"]
    rows = [["−17", "−7"], ["−9", "0"], ["−1", "7"]]
    col_w = [100, 100]
    row_h = 40
    header_h = 36
    tw = sum(col_w) + 40
    th = 16 + header_h + row_h * len(rows) + 24
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{th}" viewBox="0 0 {tw} {th}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    y = 12
    x0 = 20

    def cell(x: float, yy: float, w: float, h: float, text: str, header: bool = False) -> None:
        fill = "#f3f4f6" if header else "#fff"
        weight = "700" if header else "400"
        parts.append(
            f'<rect x="{x}" y="{yy}" width="{w}" height="{h}" fill="{fill}" stroke="#111" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{x + w / 2}" y="{yy + h / 2 + 5}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="15" font-weight="{weight}" '
            f'font-style="{"italic" if header else "normal"}">{esc(text)}</text>'
        )

    x = x0
    for i, h in enumerate(headers):
        cell(x, y, col_w[i], header_h, h, True)
        x += col_w[i]
    y += header_h
    for r in rows:
        x = x0
        for i, val in enumerate(r):
            cell(x, y, col_w[i], row_h, val, False)
            x += col_w[i]
        y += row_h
    parts.append("</svg>")
    write("math1-q22-gx-table.svg", "\n".join(parts))


def main() -> None:
    math1_q05_triangle()
    math1_q09_parallel()
    math1_q12_inequality()
    math1_q14_scatter()
    math1_q22_table()


if __name__ == "__main__":
    main()
