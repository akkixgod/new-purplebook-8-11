#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2025 August US V3 Math Module 2."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-august-us-v3/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Georgia, serif"
ARIAL = "Arial, sans-serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def q04_table() -> str:
    rows = [("x", "g(x)"), ("1", "52"), ("2", "49"), ("3", "46"), ("4", "43")]
    w, h = 220, 160
    col_w = [80, 80]
    x0, y0 = 30, 20
    row_h = 26
    parts = [f'<rect width="100%" height="100%" fill="#fff"/>']
    for i, (a, b) in enumerate(rows):
        y = y0 + i * row_h
        weight = "bold" if i == 0 else "normal"
        parts.append(
            f'<rect x="{x0}" y="{y}" width="{col_w[0]}" height="{row_h}" '
            f'fill="none" stroke="#111" stroke-width="1.2"/>'
        )
        parts.append(
            f'<rect x="{x0 + col_w[0]}" y="{y}" width="{col_w[1]}" height="{row_h}" '
            f'fill="none" stroke="#111" stroke-width="1.2"/>'
        )
        parts.append(
            f'<text x="{x0 + col_w[0]/2}" y="{y + 18}" text-anchor="middle" '
            f'font-family="{ARIAL}" font-size="14" font-weight="{weight}">{a}</text>'
        )
        parts.append(
            f'<text x="{x0 + col_w[0] + col_w[1]/2}" y="{y + 18}" text-anchor="middle" '
            f'font-family="{ARIAL}" font-size="14" font-weight="{weight}">{b}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {"".join(parts)}
</svg>'''


def q12_triangle() -> str:
    W, H = 280, 240
    # right angle bottom-left, top vertex with x°, base=53, hyp=63
    Ax, Ay = 50, 190  # right angle
    Bx, By = 50, 40   # top (angle x)
    Cx, Cy = 230, 190  # bottom-right
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="{Ax},{Ay} {Bx},{By} {Cx},{Cy}" fill="none" stroke="#111" stroke-width="2"/>
  <rect x="{Ax}" y="{Ay - 16}" width="16" height="16" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="{Bx + 14}" y="{By + 28}" font-family="{ARIAL}" font-size="14">x°</text>
  <text x="{(Ax + Cx) / 2}" y="{Ay + 22}" text-anchor="middle" font-family="{ARIAL}" font-size="14">53</text>
  <text x="{(Bx + Cx) / 2 + 14}" y="{(By + Cy) / 2}" font-family="{ARIAL}" font-size="14">63</text>
  <text x="{W / 2}" y="{H - 12}" text-anchor="middle" font-family="{ARIAL}" font-size="12">Note: Figure not drawn to scale.</text>
</svg>'''


def q15_parabola() -> str:
    W, H = 400, 300
    pad_l, pad_r, pad_t, pad_b = 40, 24, 20, 36
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = 0.0, 16.0
    ymin, ymax = 0.0, 10.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = [f'<rect width="100%" height="100%" fill="#fff"/>']
    for i in range(0, 17):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" stroke="#eee"/>'
        )
        if i % 2 == 0:
            parts.append(
                f'<text x="{sx(i)}" y="{sy(0) + 14}" text-anchor="middle" '
                f'font-family="{ARIAL}" font-size="11">{i}</text>'
            )
    for j in range(0, 11):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l + plot_w}" y2="{sy(j)}" stroke="#eee"/>'
        )
        if j % 2 == 0:
            parts.append(
                f'<text x="{sx(0) - 6}" y="{sy(j) + 4}" text-anchor="end" '
                f'font-family="{ARIAL}" font-size="11">{j}</text>'
            )
    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l + plot_w}" y2="{sy(0)}" '
        f'stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t + plot_h}" '
        f'stroke="#111" stroke-width="1.5"/>'
    )
    # y = -0.25(x-8)^2 + 4
    pts = []
    for i in range(0, 201):
        x = 2.0 + 12.0 * i / 200
        y = -0.25 * (x - 8) ** 2 + 4
        if ymin <= y <= ymax:
            pts.append(f"{sx(x):.2f},{sy(y):.2f}")
    parts.append(
        f'<polyline points="{" ".join(pts)}" fill="none" stroke="#111" stroke-width="2.2"/>'
    )
    parts.append(
        f'<text x="{pad_l + plot_w - 4}" y="{sy(0) - 8}" text-anchor="end" '
        f'font-family="{ARIAL}" font-size="13" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 10}" y="{pad_t + 14}" text-anchor="start" '
        f'font-family="{ARIAL}" font-size="13" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  {"".join(parts)}
</svg>'''


def q19_triangles() -> str:
    W, H = 420, 260
    # P--R--T on base; Q above P; S above T
    Px, Py = 60, 180
    Rx, Ry = 200, 180
    Tx, Ty = 340, 180
    Qx, Qy = 60, 50
    Sx, Sy = 340, 80
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <line x1="{Px}" y1="{Py}" x2="{Tx}" y2="{Ty}" stroke="#111" stroke-width="2"/>
  <polygon points="{Qx},{Qy} {Px},{Py} {Rx},{Ry}" fill="none" stroke="#111" stroke-width="2"/>
  <polygon points="{Sx},{Sy} {Tx},{Ty} {Rx},{Ry}" fill="none" stroke="#111" stroke-width="2"/>
  <rect x="{Px}" y="{Py - 14}" width="14" height="14" fill="none" stroke="#111" stroke-width="1.4"/>
  <rect x="{Tx - 14}" y="{Ty - 14}" width="14" height="14" fill="none" stroke="#111" stroke-width="1.4"/>
  <text x="{Qx - 16}" y="{Qy + 6}" font-family="{FONT}" font-size="16">Q</text>
  <text x="{Px - 16}" y="{Py + 20}" font-family="{FONT}" font-size="16">P</text>
  <text x="{Rx - 4}" y="{Ry + 22}" font-family="{FONT}" font-size="16">R</text>
  <text x="{Tx + 8}" y="{Ty + 20}" font-family="{FONT}" font-size="16">T</text>
  <text x="{Sx + 10}" y="{Sy + 6}" font-family="{FONT}" font-size="16">S</text>
  <text x="{Rx - 36}" y="{Ry - 18}" font-family="{ARIAL}" font-size="13">x°</text>
  <text x="{Rx + 18}" y="{Ry - 18}" font-family="{ARIAL}" font-size="13">x°</text>
  <text x="{W / 2}" y="{H - 14}" text-anchor="middle" font-family="{ARIAL}" font-size="12">Note: Figure not drawn to scale.</text>
</svg>'''


def q23_pipe() -> str:
    W, H = 320, 340
    # simple isometric-ish hollow cylinder
    cx = 160
    top_y = 70
    bot_y = 250
    rx_out, ry_out = 70, 22
    rx_in, ry_in = 48, 15
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <ellipse cx="{cx}" cy="{bot_y}" rx="{rx_out}" ry="{ry_out}" fill="none" stroke="#111" stroke-width="2"/>
  <line x1="{cx - rx_out}" y1="{top_y}" x2="{cx - rx_out}" y2="{bot_y}" stroke="#111" stroke-width="2"/>
  <line x1="{cx + rx_out}" y1="{top_y}" x2="{cx + rx_out}" y2="{bot_y}" stroke="#111" stroke-width="2"/>
  <ellipse cx="{cx}" cy="{top_y}" rx="{rx_out}" ry="{ry_out}" fill="#fff" stroke="#111" stroke-width="2"/>
  <ellipse cx="{cx}" cy="{top_y}" rx="{rx_in}" ry="{ry_in}" fill="#fff" stroke="#111" stroke-width="1.6"/>
  <line x1="{cx - rx_out}" y1="{top_y}" x2="{cx + rx_out}" y2="{top_y}" stroke="#111" stroke-width="1"/>
  <text x="{cx}" y="{top_y - 34}" text-anchor="middle" font-family="{ARIAL}" font-size="12">outside diameter</text>
  <line x1="{cx - rx_out}" y1="{top_y - 20}" x2="{cx + rx_out}" y2="{top_y - 20}" stroke="#111" stroke-width="1"/>
  <line x1="{cx - rx_out}" y1="{top_y - 24}" x2="{cx - rx_out}" y2="{top_y - 16}" stroke="#111"/>
  <line x1="{cx + rx_out}" y1="{top_y - 24}" x2="{cx + rx_out}" y2="{top_y - 16}" stroke="#111"/>
  <text x="{cx + rx_out + 8}" y="{top_y + 4}" font-family="{ARIAL}" font-size="11">wall</text>
  <text x="{cx + rx_out + 8}" y="{top_y + 18}" font-family="{ARIAL}" font-size="11">thickness</text>
  <line x1="{cx + rx_in + 4}" y1="{top_y}" x2="{cx + rx_out + 4}" y2="{top_y}" stroke="#111" stroke-width="1"/>
  <text x="{cx + rx_out + 18}" y="{(top_y + bot_y) / 2}" font-family="{ARIAL}" font-size="12">height</text>
  <line x1="{cx + rx_out + 10}" y1="{top_y}" x2="{cx + rx_out + 10}" y2="{bot_y}" stroke="#111" stroke-width="1"/>
  <line x1="{cx + rx_out + 6}" y1="{top_y}" x2="{cx + rx_out + 14}" y2="{top_y}" stroke="#111"/>
  <line x1="{cx + rx_out + 6}" y1="{bot_y}" x2="{cx + rx_out + 14}" y2="{bot_y}" stroke="#111"/>
  <text x="{W / 2}" y="{H - 14}" text-anchor="middle" font-family="{ARIAL}" font-size="12">Note: Figure not drawn to scale.</text>
</svg>'''


def q26_w_graph() -> str:
    W, H = 400, 320
    pad_l, pad_r, pad_t, pad_b = 40, 24, 20, 36
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = -10.0, 10.0
    ymin, ymax = 0.0, 12.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = [f'<rect width="100%" height="100%" fill="#fff"/>']
    for i in range(-10, 11):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" stroke="#eee"/>'
        )
        if i % 2 == 0:
            parts.append(
                f'<text x="{sx(i)}" y="{sy(0) + 14}" text-anchor="middle" '
                f'font-family="{ARIAL}" font-size="11">{i}</text>'
            )
    for j in range(0, 13):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l + plot_w}" y2="{sy(j)}" stroke="#eee"/>'
        )
        if j % 2 == 0:
            parts.append(
                f'<text x="{sx(0) - 6}" y="{sy(j) + 4}" text-anchor="end" '
                f'font-family="{ARIAL}" font-size="11">{j}</text>'
            )
    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l + plot_w}" y2="{sy(0)}" '
        f'stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t + plot_h}" '
        f'stroke="#111" stroke-width="1.5"/>'
    )
    # W shape: approx y = 0.04(x^2-25)^2/25 + 2, scaled to hit (0,7)
    # At x=0: want 7; at x=±5: want ~2
    # y = a(x^2 - 25)^2 + 2 with a*625 + 2 = 7 ⇒ a = 5/625 = 0.008
    pts = []
    for i in range(0, 201):
        x = -9.5 + 19.0 * i / 200
        y = 0.008 * (x * x - 25) ** 2 + 2
        if ymin <= y <= ymax:
            pts.append(f"{sx(x):.2f},{sy(y):.2f}")
    parts.append(
        f'<polyline points="{" ".join(pts)}" fill="none" stroke="#111" stroke-width="2.2"/>'
    )
    parts.append(
        f'<text x="{pad_l + plot_w - 4}" y="{sy(0) - 8}" text-anchor="end" '
        f'font-family="{ARIAL}" font-size="13" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 10}" y="{pad_t + 14}" text-anchor="start" '
        f'font-family="{ARIAL}" font-size="13" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  {"".join(parts)}
</svg>'''


def q28_tables() -> str:
    W, H = 480, 220

    def table(x0: int, title: str, freqs: list[str]) -> list[str]:
        parts = [
            f'<text x="{x0 + 90}" y="28" text-anchor="middle" font-family="{FONT}" '
            f'font-size="15" font-weight="bold">{title}</text>'
        ]
        headers = [("Value", "Frequency")]
        rows = headers + [("c", freqs[0]), ("2c", freqs[1]), ("3c", freqs[2])]
        col_w = [80, 100]
        y0 = 40
        row_h = 28
        for i, (a, b) in enumerate(rows):
            y = y0 + i * row_h
            weight = "bold" if i == 0 else "normal"
            parts.append(
                f'<rect x="{x0}" y="{y}" width="{col_w[0]}" height="{row_h}" '
                f'fill="none" stroke="#111" stroke-width="1.2"/>'
            )
            parts.append(
                f'<rect x="{x0 + col_w[0]}" y="{y}" width="{col_w[1]}" height="{row_h}" '
                f'fill="none" stroke="#111" stroke-width="1.2"/>'
            )
            parts.append(
                f'<text x="{x0 + col_w[0]/2}" y="{y + 19}" text-anchor="middle" '
                f'font-family="{ARIAL}" font-size="14" font-weight="{weight}">{a}</text>'
            )
            parts.append(
                f'<text x="{x0 + col_w[0] + col_w[1]/2}" y="{y + 19}" text-anchor="middle" '
                f'font-family="{ARIAL}" font-size="14" font-weight="{weight}">{b}</text>'
            )
        return parts

    parts = [f'<rect width="100%" height="100%" fill="#fff"/>']
    parts.extend(table(40, "Data Set A", ["12", "21", "30"]))
    parts.extend(table(260, "Data Set B", ["30", "21", "12"]))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  {"".join(parts)}
</svg>'''


def main() -> None:
    write("math2-q04-gx-table.svg", q04_table())
    write("math2-q12-right-triangle.svg", q12_triangle())
    write("math2-q15-parabola.svg", q15_parabola())
    write("math2-q19-similar-triangles.svg", q19_triangles())
    write("math2-q23-hollow-pipe.svg", q23_pipe())
    write("math2-q26-w-graph.svg", q26_w_graph())
    write("math2-q28-frequency-tables.svg", q28_tables())


if __name__ == "__main__":
    main()
