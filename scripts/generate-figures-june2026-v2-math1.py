#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2026 June V2 Math Module 1."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2026-june-v2/figures")
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
    row_labels_bold: bool = False,
    header_fill: str = "#f3f4f6",
    first_col_fill: str | None = "#f3f4f6",
) -> str:
    widths = col_widths
    width = sum(widths) + 40
    needs_wrap = any("|" in h for h in headers)
    hh = header_h if header_h is not None else (52 if needs_wrap else 40)
    rh = row_h if row_h is not None else 40
    height = 20 + hh + rh * len(rows) + 20
    x0, y0 = 20, 20
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{hh}" '
            f'fill="{header_fill}" stroke="#111"/>'
        )
        if "|" in h:
            lines = h.split("|")
            line_h = 14
            start_y = y0 + (hh - line_h * (len(lines) - 1)) / 2 - 2
            for li, line in enumerate(lines):
                cells.append(
                    f'<text x="{x + widths[i] / 2}" y="{start_y + li * line_h}" '
                    f'text-anchor="middle" font-family="{FONT}" '
                    f'font-size="{header_font}" font-weight="700">{line}</text>'
                )
        else:
            italic = ' font-style="italic"' if h in {"x", "y", "r", "g"} else ""
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
            weight = ' font-weight="700"' if (row_labels_bold and i == 0) else ""
            anchor = "middle"
            tx = x + widths[i] / 2
            if i == 0 and row_labels_bold:
                anchor = "start"
                tx = x + 10
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{rh}" '
                f'fill="{fill}" stroke="#111"/>'
                f'<text x="{tx}" y="{y + rh / 2 + 4}" text-anchor="{anchor}" '
                f'font-family="{FONT}" font-size="{font_size}"{weight}>{cell}</text>'
            )
            x += widths[i]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(cells)}
</svg>'''


def math1_q01_member_table() -> str:
    return table_svg(
        ["", "Live north of|Center St.", "Live south of|Center St.", "Total"],
        [
            ["Less than 45 years old", "15", "10", "25"],
            ["At least 45 years old", "20", "90", "110"],
            ["Total", "35", "100", "135"],
        ],
        [190, 120, 120, 80],
        header_font=12,
        font_size=13,
        header_h=52,
        row_h=42,
        row_labels_bold=True,
    )


def math1_q03_rg_tables() -> str:
    """Four choice tables for r + g < 39."""
    tables = {
        "A": [("0", "34"), ("2", "36"), ("4", "38")],
        "B": [("0", "34"), ("2", "38"), ("4", "36")],
        "C": [("0", "36"), ("2", "38"), ("4", "34")],
        "D": [("0", "38"), ("2", "36"), ("4", "34")],
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
        for j, h in enumerate(["r", "g"]):
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


def math1_q12_right_triangle() -> str:
    """Right triangle: horizontal leg 4.5, vertical leg 2.4, hypotenuse x."""
    # scale: 4.5 → 270px, 2.4 → 144px
    bl, br, tr = (80, 220), (350, 220), (350, 76)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="440" height="300" viewBox="0 0 440 300">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="{bl[0]},{bl[1]} {br[0]},{br[1]} {tr[0]},{tr[1]}" fill="none" stroke="#111" stroke-width="2"/>
  <rect x="{br[0] - 18}" y="{br[1] - 18}" width="18" height="18" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="{(bl[0] + br[0]) / 2}" y="{bl[1] + 28}" text-anchor="middle" font-family="{FONT}" font-size="18">4.5</text>
  <text x="{br[0] + 28}" y="{(br[1] + tr[1]) / 2 + 6}" text-anchor="middle" font-family="{FONT}" font-size="18">2.4</text>
  <text x="{(bl[0] + tr[0]) / 2 - 8}" y="{(bl[1] + tr[1]) / 2}" text-anchor="middle" font-family="{FONT}" font-size="18" font-style="italic">x</text>
  <text x="220" y="280" text-anchor="middle" font-family="{FONT}" font-size="13">Note: Figure not drawn to scale.</text>
</svg>'''


def math1_q13_exponential() -> str:
    """y = 3^x + 7 on grid x∈[-8,8], y∈[0,14]."""
    W, H = 520, 420
    pad_l, pad_r, pad_t, pad_b = 44, 36, 28, 40
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = -8.0, 8.0
    ymin, ymax = 0.0, 14.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = []
    for i in range(int(xmin), int(xmax) + 1):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" '
            f'stroke="#e5e7eb"/>'
        )
    for j in range(int(ymin), int(ymax) + 1):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l + plot_w}" y2="{sy(j)}" '
            f'stroke="#e5e7eb"/>'
        )
    # axes
    parts.append(
        f'<line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t + plot_h}" '
        f'stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l + plot_w}" y2="{sy(0)}" '
        f'stroke="#111" stroke-width="1.5"/>'
    )
    # curve y = 3^x + 7
    pts: list[str] = []
    x = xmin
    while x <= xmax + 1e-9:
        y = 3**x + 7
        if ymin <= y <= ymax + 0.5:
            yy = min(y, ymax)
            pts.append(f"{sx(x):.2f},{sy(yy):.2f}")
        x += 0.05
    parts.append(
        f'<polyline points="{" ".join(pts)}" fill="none" stroke="#111" stroke-width="2.2"/>'
    )
    for i in range(int(xmin), int(xmax) + 1, 2):
        parts.append(
            f'<text x="{sx(i)}" y="{pad_t + plot_h + 18}" text-anchor="middle" '
            f'font-family="Arial" font-size="12">{i}</text>'
        )
    for j in range(2, int(ymax) + 1, 2):
        parts.append(
            f'<text x="{pad_l - 8}" y="{sy(j) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="12">{j}</text>'
        )
    parts.append(
        f'<text x="{pad_l + plot_w + 8}" y="{sy(0) + 4}" font-family="Arial" '
        f'font-size="14" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 8}" y="{pad_t - 6}" font-family="Arial" '
        f'font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q18_xy_table() -> str:
    return table_svg(
        ["x", "y"],
        [
            ["−10", "n + 106"],
            ["−5", "n + 53"],
            ["0", "n"],
        ],
        [100, 120],
        font_size=15,
        header_font=15,
        header_h=40,
        row_h=40,
        row_labels_bold=False,
        first_col_fill=None,
    )


def math1_q20_line_segment() -> str:
    """Line segment from (0, 7) to (5, 0) on 0–10 axes."""
    W, H = 440, 440
    pad_l, pad_r, pad_t, pad_b = 40, 36, 28, 40
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmax = ymax = 10.0

    def sx(x: float) -> float:
        return pad_l + (x / xmax) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / ymax) * plot_h

    parts: list[str] = []
    for i in range(0, 11):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" '
            f'stroke="#e5e7eb"/>'
        )
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(i)}" x2="{pad_l + plot_w}" y2="{sy(i)}" '
            f'stroke="#e5e7eb"/>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" '
        f'stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" '
        f'y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{sy(7)}" x2="{sx(5)}" y2="{sy(0)}" '
        f'stroke="#111" stroke-width="2.5"/>'
    )
    parts.append(f'<circle cx="{sx(0)}" cy="{sy(7)}" r="4.5" fill="#111"/>')
    parts.append(f'<circle cx="{sx(5)}" cy="{sy(0)}" r="4.5" fill="#111"/>')
    for i in range(1, 11):
        parts.append(
            f'<text x="{sx(i)}" y="{pad_t + plot_h + 18}" text-anchor="middle" '
            f'font-family="Arial" font-size="12">{i}</text>'
        )
        parts.append(
            f'<text x="{pad_l - 8}" y="{sy(i) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="12">{i}</text>'
        )
    parts.append(
        f'<text x="{pad_l + plot_w + 10}" y="{pad_t + plot_h + 4}" '
        f'font-family="Arial" font-size="14" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{pad_l - 4}" y="{pad_t - 8}" font-family="Arial" '
        f'font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def main() -> None:
    write("math1-q01-member-table.svg", math1_q01_member_table())
    write("math1-q03-rg-tables.svg", math1_q03_rg_tables())
    write("math1-q12-right-triangle.svg", math1_q12_right_triangle())
    write("math1-q13-exponential.svg", math1_q13_exponential())
    write("math1-q18-xy-table.svg", math1_q18_xy_table())
    write("math1-q20-line-segment.svg", math1_q20_line_segment())


if __name__ == "__main__":
    main()
