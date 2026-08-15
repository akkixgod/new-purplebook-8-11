#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2025 June US-A Math Module 2."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-june-us-a/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Georgia, serif"
ARIAL = "Arial, sans-serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def math2_q02_revenue_graph() -> str:
    """Downward parabola: Revenue vs Price. Vertex (~25, ~625), intercepts 0 and 50."""
    W, H = 440, 380
    pad_l, pad_r, pad_t, pad_b = 70, 36, 28, 56
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = 0.0, 100.0
    ymin, ymax = 0.0, 2000.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    # Light grid
    for i in range(0, 11):
        x = i * 10
        parts.append(
            f'<line x1="{sx(x):.1f}" y1="{pad_t}" x2="{sx(x):.1f}" y2="{pad_t + plot_h}" stroke="#eee"/>'
        )
    for j in range(0, 11):
        y = j * 200
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(y):.1f}" x2="{pad_l + plot_w}" y2="{sy(y):.1f}" stroke="#eee"/>'
        )
    # Axes
    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l + plot_w}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    # Axis ticks / labels
    for x in (0, 20, 40, 60, 80, 100):
        parts.append(
            f'<line x1="{sx(x):.1f}" y1="{sy(0)}" x2="{sx(x):.1f}" y2="{sy(0) + 5}" stroke="#111"/>'
        )
        parts.append(
            f'<text x="{sx(x):.1f}" y="{sy(0) + 18}" text-anchor="middle" '
            f'font-family="{ARIAL}" font-size="11">{x}</text>'
        )
    for y in (0, 400, 800, 1200, 1600, 2000):
        parts.append(
            f'<line x1="{sx(0) - 5}" y1="{sy(y):.1f}" x2="{sx(0)}" y2="{sy(y):.1f}" stroke="#111"/>'
        )
        label = f"{y:,}"
        parts.append(
            f'<text x="{sx(0) - 8}" y="{sy(y) + 4:.1f}" text-anchor="end" '
            f'font-family="{ARIAL}" font-size="11">{label}</text>'
        )
    # Curve y = x(50 - x) on [0, 50], then continue slightly
    pts = []
    for i in range(0, 101):
        x = 50.0 * i / 100
        y = x * (50 - x)
        pts.append(f"{sx(x):.2f},{sy(y):.2f}")
    parts.append(
        f'<polyline points="{" ".join(pts)}" fill="none" stroke="#111" stroke-width="2.2"/>'
    )
    # Vertex marker
    parts.append(f'<circle cx="{sx(25):.2f}" cy="{sy(625):.2f}" r="4" fill="#111"/>')
    parts.append(
        f'<text x="{W / 2}" y="{H - 8}" text-anchor="middle" font-family="{ARIAL}" font-size="12">Price (dollars)</text>'
    )
    parts.append(
        f'<text x="16" y="{H / 2}" text-anchor="middle" font-family="{ARIAL}" font-size="12" '
        f'transform="rotate(-90 16 {H / 2})">Revenue (dollars)</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def math2_q03_xy_table() -> str:
    """Table: x | y with rows (0,95), (1,105), (2,115)."""
    rows = [("0", "95"), ("1", "105"), ("2", "115")]
    cell_w, cell_h = 80, 40
    ox, oy = 40, 20
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="240" height="200" viewBox="0 0 240 200">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<rect x="{ox}" y="{oy}" width="{cell_w}" height="{cell_h}" fill="#f3f4f6" stroke="#111"/>',
        f'<text x="{ox + cell_w / 2}" y="{oy + 26}" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="700">x</text>',
        f'<rect x="{ox + cell_w}" y="{oy}" width="{cell_w}" height="{cell_h}" fill="#f3f4f6" stroke="#111"/>',
        f'<text x="{ox + cell_w * 1.5}" y="{oy + 26}" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="700">y</text>',
    ]
    for i, (xv, yv) in enumerate(rows):
        y = oy + cell_h * (i + 1)
        parts.append(
            f'<rect x="{ox}" y="{y}" width="{cell_w}" height="{cell_h}" fill="#fff" stroke="#111"/>'
        )
        parts.append(
            f'<text x="{ox + cell_w / 2}" y="{y + 26}" text-anchor="middle" font-family="{FONT}" font-size="15">{xv}</text>'
        )
        parts.append(
            f'<rect x="{ox + cell_w}" y="{y}" width="{cell_w}" height="{cell_h}" fill="#fff" stroke="#111"/>'
        )
        parts.append(
            f'<text x="{ox + cell_w * 1.5}" y="{y + 26}" text-anchor="middle" font-family="{FONT}" font-size="15">{yv}</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def math2_q09_parallel_angles() -> str:
    """Trapezoid-like figure: S-T-W collinear, TU || VW, angles p° at U and r° at W."""
    # Layout: S above T, W below on left slanted line; U top-right; V bottom-right
    Sx, Sy = 120, 40
    Tx, Ty = 140, 110
    Wx, Wy = 170, 220
    Ux, Uy = 300, 110
    Vx, Vy = 310, 220
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="380" height="300" viewBox="0 0 380 300">
  <rect width="100%" height="100%" fill="#fff"/>
  <!-- Line S-T-W -->
  <line x1="{Sx}" y1="{Sy}" x2="{Wx}" y2="{Wy}" stroke="#111" stroke-width="2"/>
  <!-- TU parallel VW -->
  <line x1="{Tx}" y1="{Ty}" x2="{Ux}" y2="{Uy}" stroke="#111" stroke-width="2"/>
  <line x1="{Wx}" y1="{Wy}" x2="{Vx}" y2="{Vy}" stroke="#111" stroke-width="2"/>
  <!-- UV side -->
  <line x1="{Ux}" y1="{Uy}" x2="{Vx}" y2="{Vy}" stroke="#111" stroke-width="2"/>
  <!-- Labels -->
  <text x="{Sx - 18}" y="{Sy + 6}" font-family="{FONT}" font-size="16">S</text>
  <text x="{Tx - 20}" y="{Ty + 6}" font-family="{FONT}" font-size="16">T</text>
  <text x="{Ux + 10}" y="{Uy + 6}" font-family="{FONT}" font-size="16">U</text>
  <text x="{Vx + 10}" y="{Vy + 6}" font-family="{FONT}" font-size="16">V</text>
  <text x="{Wx - 22}" y="{Wy + 8}" font-family="{FONT}" font-size="16">W</text>
  <!-- Angle marks: p at U, r at W -->
  <path d="M {Ux - 28} {Uy} A 28 28 0 0 1 {Ux - 8} {Uy + 26}" fill="none" stroke="#111" stroke-width="1.4"/>
  <text x="{Ux - 48}" y="{Uy + 28}" font-family="{ARIAL}" font-size="14">p°</text>
  <path d="M {Wx + 28} {Wy} A 28 28 0 0 0 {Wx + 10} {Wy - 26}" fill="none" stroke="#111" stroke-width="1.4"/>
  <text x="{Wx + 32}" y="{Wy - 18}" font-family="{ARIAL}" font-size="14">r°</text>
  <text x="190" y="285" text-anchor="middle" font-family="{ARIAL}" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math2_q11_shaded_inequality() -> str:
    """xy-plane, dashed horizontal line y=-8, shaded region above (y > -8)."""
    W, H = 420, 360
    pad_l, pad_r, pad_t, pad_b = 44, 28, 24, 36
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = -8.0, 8.0
    ymin, ymax = -10.0, 2.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for i in range(-8, 9):
        parts.append(
            f'<line x1="{sx(i):.1f}" y1="{pad_t}" x2="{sx(i):.1f}" y2="{pad_t + plot_h}" stroke="#eee"/>'
        )
    for j in range(-10, 3, 2):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j):.1f}" x2="{pad_l + plot_w}" y2="{sy(j):.1f}" stroke="#eee"/>'
        )
    # Shaded region y > -8 (above the dashed line on screen = smaller sy)
    y_line = sy(-8)
    parts.append(
        f'<rect x="{pad_l}" y="{pad_t}" width="{plot_w}" height="{y_line - pad_t:.1f}" fill="#d1d5db" fill-opacity="0.55"/>'
    )
    # Axes
    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l + plot_w}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    # Dashed boundary
    parts.append(
        f'<line x1="{pad_l}" y1="{y_line:.1f}" x2="{pad_l + plot_w}" y2="{y_line:.1f}" '
        f'stroke="#111" stroke-width="2" stroke-dasharray="6 4"/>'
    )
    for i in range(-8, 9, 2):
        if i == 0:
            continue
        parts.append(
            f'<text x="{sx(i):.1f}" y="{sy(0) + 14}" text-anchor="middle" font-family="{ARIAL}" font-size="11">{i}</text>'
        )
    for j in range(-10, 3, 2):
        if j == 0:
            continue
        parts.append(
            f'<text x="{sx(0) - 6}" y="{sy(j) + 4:.1f}" text-anchor="end" font-family="{ARIAL}" font-size="11">{j}</text>'
        )
    parts.append(
        f'<text x="{pad_l + plot_w - 4}" y="{sy(0) - 8}" text-anchor="end" font-family="{ARIAL}" font-size="13" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 8}" y="{pad_t + 12}" font-family="{ARIAL}" font-size="13" font-style="italic">y</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def math2_q15_line_graph() -> str:
    """Line through (0,-5) and (3,0)."""
    W, H = 420, 380
    pad_l, pad_r, pad_t, pad_b = 44, 28, 24, 36
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = -1.0, 9.0
    ymin, ymax = -9.0, 1.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for i in range(-1, 10):
        parts.append(
            f'<line x1="{sx(i):.1f}" y1="{pad_t}" x2="{sx(i):.1f}" y2="{pad_t + plot_h}" stroke="#eee"/>'
        )
    for j in range(-9, 2):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j):.1f}" x2="{pad_l + plot_w}" y2="{sy(j):.1f}" stroke="#eee"/>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l + plot_w}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="2"/>'
    )
    # Line through (0,-5) and (3,0); extend across plot: y = (5/3)x - 5
    x1, x2 = xmin, xmax
    y1 = (5 / 3) * x1 - 5
    y2 = (5 / 3) * x2 - 5
    # clip to plot y range visually
    parts.append(
        f'<line x1="{sx(x1):.2f}" y1="{sy(y1):.2f}" x2="{sx(x2):.2f}" y2="{sy(y2):.2f}" '
        f'stroke="#111" stroke-width="2.2"/>'
    )
    for i in range(0, 10):
        if i == 0:
            continue
        parts.append(
            f'<text x="{sx(i):.1f}" y="{sy(0) + 14}" text-anchor="middle" font-family="{ARIAL}" font-size="11">{i}</text>'
        )
    for j in range(-9, 2):
        if j == 0:
            continue
        parts.append(
            f'<text x="{sx(0) - 6}" y="{sy(j) + 4:.1f}" text-anchor="end" font-family="{ARIAL}" font-size="11">{j}</text>'
        )
    parts.append(
        f'<text x="{pad_l + plot_w - 4}" y="{sy(0) - 8}" text-anchor="end" font-family="{ARIAL}" font-size="13" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 8}" y="{pad_t + 12}" font-family="{ARIAL}" font-size="13" font-style="italic">y</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    write("math2-q02-revenue-graph.svg", math2_q02_revenue_graph())
    write("math2-q03-xy-table.svg", math2_q03_xy_table())
    write("math2-q09-parallel-angles.svg", math2_q09_parallel_angles())
    write("math2-q11-shaded-inequality.svg", math2_q11_shaded_inequality())
    write("math2-q15-line-graph.svg", math2_q15_line_graph())


if __name__ == "__main__":
    main()
