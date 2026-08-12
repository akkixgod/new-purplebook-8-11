#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2026 June V3 Math Module 1."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2026-june-v3/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Georgia, serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def table_svg(
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[int],
    *,
    font_size: int = 13,
    header_font: int = 12,
    row_h: int | None = None,
    header_h: int | None = None,
    first_col_fill: str | None = None,
) -> str:
    widths = col_widths
    width = sum(widths) + 40
    hh = header_h if header_h is not None else 40
    rh = row_h if row_h is not None else 40
    height = 20 + hh + rh * len(rows) + 20
    x0, y0 = 20, 20
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{hh}" '
            f'fill="#f3f4f6" stroke="#111"/>'
        )
        italic = ' font-style="italic"' if h in {"x", "y"} else ""
        cells.append(
            f'<text x="{x + widths[i] / 2}" y="{y0 + hh / 2 + 4}" '
            f'text-anchor="middle" font-family="{FONT}" '
            f'font-size="{header_font}" font-weight="700"{italic}>{h}</text>'
        )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + hh + rh * r
        x = x0
        for i, cell in enumerate(row):
            fill = first_col_fill if (i == 0 and first_col_fill) else "#fff"
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{rh}" '
                f'fill="{fill}" stroke="#111"/>'
                f'<text x="{x + widths[i] / 2}" y="{y + rh / 2 + 4}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="{font_size}">{cell}</text>'
            )
            x += widths[i]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(cells)}
</svg>'''


def math1_q03_xy_tables() -> str:
    """Four choice tables for y = 30x + 6."""
    tables = {
        "A": [("0", "30"), ("2", "60"), ("4", "120")],
        "B": [("0", "6"), ("2", "66"), ("4", "126")],
        "C": [("0", "6"), ("2", "54"), ("4", "114")],
        "D": [("0", "30"), ("2", "36"), ("4", "42")],
    }
    tw, th = 90, 34
    parts: list[str] = []
    for i, (lab, rows) in enumerate(tables.items()):
        y0 = 16 + i * 160
        parts.append(
            f'<circle cx="26" cy="{y0 + 68}" r="12" fill="none" stroke="#111" stroke-width="1.5"/>'
            f'<text x="26" y="{y0 + 73}" text-anchor="middle" font-family="Arial, sans-serif" '
            f'font-size="14">{lab}</text>'
        )
        x0 = 50
        for j, h in enumerate(["x", "y"]):
            parts.append(
                f'<rect x="{x0 + j * tw}" y="{y0}" width="{tw}" height="{th}" '
                f'fill="#e8eef5" stroke="#111"/>'
                f'<text x="{x0 + j * tw + tw / 2}" y="{y0 + 23}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="14" font-style="italic" '
                f'font-weight="700">{h}</text>'
            )
        for r, (xv, yv) in enumerate(rows):
            yy = y0 + th * (r + 1)
            for j, val in enumerate([xv, yv]):
                parts.append(
                    f'<rect x="{x0 + j * tw}" y="{yy}" width="{tw}" height="{th}" '
                    f'fill="#fff" stroke="#111"/>'
                    f'<text x="{x0 + j * tw + tw / 2}" y="{yy + 23}" text-anchor="middle" '
                    f'font-family="{FONT}" font-size="14">{val}</text>'
                )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="260" height="660" viewBox="0 0 260 660">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q12_triangle() -> str:
    """Right triangle ABC at A; DE || AC with D on AB, E on BC."""
    # A bottom-left, B top-left, C bottom-right
    A, B, C = (80, 280), (80, 60), (360, 280)
    # D midpoint of AB; E on BC at half the similarity ratio from B
    D = (80, 170)
    # E is midpoint of BC if DE || AC and D midpoint of AB
    E = ((B[0] + C[0]) / 2, (B[1] + C[1]) / 2)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="440" height="360" viewBox="0 0 440 360">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="none" stroke="#111" stroke-width="2.5"/>
  <line x1="{D[0]}" y1="{D[1]}" x2="{E[0]}" y2="{E[1]}" stroke="#111" stroke-width="2"/>
  <rect x="{A[0]}" y="{A[1] - 16}" width="16" height="16" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="{A[0] - 22}" y="{A[1] + 18}" font-family="{FONT}" font-size="16" font-weight="700">A</text>
  <text x="{B[0] - 22}" y="{B[1] + 6}" font-family="{FONT}" font-size="16" font-weight="700">B</text>
  <text x="{C[0] + 10}" y="{C[1] + 18}" font-family="{FONT}" font-size="16" font-weight="700">C</text>
  <text x="{D[0] - 22}" y="{D[1] + 6}" font-family="{FONT}" font-size="16" font-weight="700">D</text>
  <text x="{E[0] + 10}" y="{E[1] + 4}" font-family="{FONT}" font-size="16" font-weight="700">E</text>
  <text x="220" y="340" text-anchor="middle" font-family="{FONT}" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math1_q18_tetrahedron() -> str:
    """Wireframe trirectangular tetrahedron: dashed mutually perpendicular edges."""
    # Right-angle vertex appears interior in projection; three outer vertices
    O = (200, 200)
    top = (205, 45)
    left = (70, 270)
    right = (350, 255)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="340" viewBox="0 0 420 340">
  <rect width="100%" height="100%" fill="#fff"/>
  <!-- outer face (hypotenuse triangle) -->
  <polygon points="{top[0]},{top[1]} {left[0]},{left[1]} {right[0]},{right[1]}" fill="none" stroke="#111" stroke-width="2.2"/>
  <!-- dashed mutually perpendicular legs from right-angle vertex -->
  <line x1="{O[0]}" y1="{O[1]}" x2="{top[0]}" y2="{top[1]}" stroke="#111" stroke-width="1.7" stroke-dasharray="6 4"/>
  <line x1="{O[0]}" y1="{O[1]}" x2="{left[0]}" y2="{left[1]}" stroke="#111" stroke-width="1.7" stroke-dasharray="6 4"/>
  <line x1="{O[0]}" y1="{O[1]}" x2="{right[0]}" y2="{right[1]}" stroke="#111" stroke-width="1.7" stroke-dasharray="6 4"/>
  <rect x="{O[0]}" y="{O[1] - 12}" width="12" height="12" fill="none" stroke="#111" stroke-width="1.4"/>
  <text x="210" y="320" text-anchor="middle" font-family="{FONT}" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math1_q20_line() -> str:
    """Line through (−12, 0) and (0, −11) on axes from −14 to 0."""
    W, H = 480, 480
    pad_l, pad_r, pad_t, pad_b = 48, 40, 36, 44
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = -14.0, 0.0
    ymin, ymax = -14.0, 0.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = []
    # minor grid every 1
    for i in range(-14, 1):
        stroke = "#e5e7eb" if i % 2 != 0 else "#d1d5db"
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" '
            f'stroke="{stroke}"/>'
        )
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(i)}" x2="{pad_l + plot_w}" y2="{sy(i)}" '
            f'stroke="{stroke}"/>'
        )
    # axes at x=0 and y=0 (top and right edges of this quadrant view)
    parts.append(
        f'<line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t + plot_h}" '
        f'stroke="#111" stroke-width="1.8"/>'
    )
    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l + plot_w}" y2="{sy(0)}" '
        f'stroke="#111" stroke-width="1.8"/>'
    )
    # line segment
    parts.append(
        f'<line x1="{sx(-12)}" y1="{sy(0)}" x2="{sx(0)}" y2="{sy(-11)}" '
        f'stroke="#111" stroke-width="2.5"/>'
    )
    parts.append(f'<circle cx="{sx(-12)}" cy="{sy(0)}" r="5" fill="#2563eb"/>')
    parts.append(f'<circle cx="{sx(0)}" cy="{sy(-11)}" r="5" fill="#2563eb"/>')
    for i in range(-14, 1, 2):
        parts.append(
            f'<text x="{sx(i)}" y="{pad_t + plot_h + 18}" text-anchor="middle" '
            f'font-family="Arial" font-size="11">{i}</text>'
        )
        if i != 0:
            parts.append(
                f'<text x="{pad_l - 8}" y="{sy(i) + 4}" text-anchor="end" '
                f'font-family="Arial" font-size="11">{i}</text>'
            )
    parts.append(
        f'<text x="{sx(0) + 16}" y="{sy(0) + 18}" font-family="Arial" '
        f'font-size="14" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) - 14}" y="{pad_t + 14}" font-family="Arial" '
        f'font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q21_xy_table() -> str:
    return table_svg(
        ["x", "y"],
        [
            ["0", "−2"],
            ["12", "0"],
            ["24", "2"],
        ],
        [90, 90],
        font_size=15,
        header_font=15,
        header_h=40,
        row_h=40,
    )


def main() -> None:
    write("math1-q03-xy-tables.svg", math1_q03_xy_tables())
    write("math1-q12-triangle.svg", math1_q12_triangle())
    write("math1-q18-tetrahedron.svg", math1_q18_tetrahedron())
    write("math1-q20-line.svg", math1_q20_line())
    write("math1-q21-xy-table.svg", math1_q21_xy_table())
    print("done June 2026 V3 Math Module 1 figures")


if __name__ == "__main__":
    main()
