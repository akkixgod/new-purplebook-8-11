#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2025 August US V2 Math Module 2."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-august-us-v2/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Georgia, serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def math2_q02_triangle() -> str:
    """Right triangle ABC: right angle at C, angle A=48°, AB=22."""
    W, H = 320, 280
    Cx, Cy = 70, 200
    Bx, By = 250, 200
    Ax, Ay = 70, 50
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="{Ax},{Ay} {Bx},{By} {Cx},{Cy}" fill="none" stroke="#111" stroke-width="2"/>
  <rect x="{Cx}" y="{Cy - 16}" width="16" height="16" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="{Ax - 18}" y="{Ay + 8}" font-family="{FONT}" font-size="16">A</text>
  <text x="{Bx + 8}" y="{By + 6}" font-family="{FONT}" font-size="16">B</text>
  <text x="{Cx - 18}" y="{Cy + 20}" font-family="{FONT}" font-size="16">C</text>
  <text x="{Ax + 14}" y="{Ay + 28}" font-family="Arial" font-size="13">48°</text>
  <text x="{(Ax + Bx) / 2 + 8}" y="{(Ay + By) / 2 - 4}" font-family="Arial" font-size="14">22</text>
  <text x="{W / 2}" y="{H - 14}" text-anchor="middle" font-family="Arial" font-size="12">Note: Figure not drawn to scale.</text>
</svg>'''


def math2_q06_parabola() -> str:
    """Downward parabola through (0,0), vertex (2.5, 6.25), (5,0)."""
    W, H = 420, 400
    pad_l, pad_r, pad_t, pad_b = 44, 28, 24, 36
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = -7.0, 7.0
    ymin, ymax = -10.0, 10.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = []
    for i in range(-7, 8):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" stroke="#eee"/>'
        )
        if i != 0:
            parts.append(
                f'<text x="{sx(i)}" y="{sy(0) + 14}" text-anchor="middle" '
                f'font-family="Arial" font-size="11">{i}</text>'
            )
    for j in range(-10, 11, 2):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l + plot_w}" y2="{sy(j)}" stroke="#eee"/>'
        )
        if j != 0:
            parts.append(
                f'<text x="{sx(0) - 6}" y="{sy(j) + 4}" text-anchor="end" '
                f'font-family="Arial" font-size="11">{j}</text>'
            )
    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l + plot_w}" y2="{sy(0)}" '
        f'stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t + plot_h}" '
        f'stroke="#111" stroke-width="1.5"/>'
    )
    # y = -x(x-5) = -x^2 + 5x
    pts = []
    for i in range(0, 201):
        x = -1.5 + 8.0 * i / 200
        y = -x * (x - 5)
        if ymin <= y <= ymax:
            pts.append(f"{sx(x):.2f},{sy(y):.2f}")
    parts.append(
        f'<polyline points="{" ".join(pts)}" fill="none" stroke="#111" stroke-width="2.2"/>'
    )
    for px, py in ((0, 0), (2.5, 6.25), (5, 0)):
        parts.append(f'<circle cx="{sx(px)}" cy="{sy(py)}" r="4" fill="#111"/>')
    parts.append(
        f'<text x="{pad_l + plot_w - 4}" y="{sy(0) - 8}" text-anchor="end" '
        f'font-family="Arial" font-size="13" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 10}" y="{pad_t + 14}" text-anchor="start" '
        f'font-family="Arial" font-size="13" font-style="italic">y</text>'
    )
    parts.append(
        f'<text x="{sx(0) - 10}" y="{sy(0) + 14}" text-anchor="end" '
        f'font-family="Arial" font-size="11" font-style="italic">O</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math2_q08_table() -> str:
    headers = ["x", "f(x)"]
    rows = [["−27", "7"], ["−6", "0"], ["21", "9"]]
    widths = [90, 90]
    width = sum(widths) + 40
    row_h = 36
    height = 20 + row_h * (1 + len(rows)) + 16
    x0, y0 = 20, 16
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{row_h}" '
            f'fill="#f3f4f6" stroke="#111"/>'
            f'<text x="{x + widths[i] / 2}" y="{y0 + 24}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="13" font-weight="700">{esc(h)}</text>'
        )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + row_h * (r + 1)
        x = x0
        for i, cell in enumerate(row):
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" '
                f'fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i] / 2}" y="{y + 24}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="13">{esc(cell)}</text>'
            )
            x += widths[i]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(cells)}
</svg>'''


def math2_q17_scatter() -> str:
    W, H = 460, 440
    pad_l, pad_r, pad_t, pad_b = 48, 36, 28, 40
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = -4.0, 4.0
    ymin, ymax = 0.0, 160.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = []
    for i in range(-4, 5):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" '
            f'stroke="#e5e7eb"/>'
        )
    for j in range(0, 161, 20):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l + plot_w}" y2="{sy(j)}" '
            f'stroke="#e5e7eb"/>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l + plot_w}" y2="{sy(0)}" '
        f'stroke="#111" stroke-width="1.6"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t + plot_h}" '
        f'stroke="#111" stroke-width="1.6"/>'
    )
    parts.append(
        f'<polygon points="{pad_l + plot_w},{sy(0)} {pad_l + plot_w - 8},{sy(0) - 4} '
        f'{pad_l + plot_w - 8},{sy(0) + 4}" fill="#111"/>'
    )
    parts.append(
        f'<polygon points="{sx(0)},{pad_t} {sx(0) - 4},{pad_t + 8} '
        f'{sx(0) + 4},{pad_t + 8}" fill="#111"/>'
    )
    for i in range(-4, 5):
        if i == 0:
            continue
        parts.append(
            f'<text x="{sx(i)}" y="{sy(0) + 16}" text-anchor="middle" '
            f'font-family="Arial" font-size="12">{i}</text>'
        )
    for j in (40, 80, 120, 160):
        parts.append(
            f'<text x="{sx(0) - 8}" y="{sy(j) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="12">{j}</text>'
        )
    parts.append(
        f'<text x="{pad_l + plot_w - 4}" y="{sy(0) - 10}" text-anchor="end" '
        f'font-family="Arial" font-size="13" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 10}" y="{pad_t + 14}" text-anchor="start" '
        f'font-family="Arial" font-size="13" font-style="italic">y</text>'
    )
    parts.append(
        f'<text x="{sx(0) - 10}" y="{sy(0) + 14}" text-anchor="end" '
        f'font-family="Arial" font-size="12" font-style="italic">O</text>'
    )

    points = [
        (-1.25, 147),
        (-1.0, 104),
        (-0.5, 52),
        (0.0, 26),
        (0.5, 13),
        (1.0, 6),
        (1.5, 3),
        (2.0, 2),
        (2.5, 1),
        (3.0, 1),
    ]
    for xi, yi in points:
        parts.append(
            f'<circle cx="{sx(xi):.2f}" cy="{sy(yi):.2f}" r="4.5" fill="#111"/>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def _freq_table(
    x0: float,
    y0: float,
    label: str,
    freqs: list[int],
) -> list[str]:
    eggs = [7, 8, 9, 10, 11]
    widths = [120, 100]
    row_h = 28
    header_h = 32
    cells: list[str] = []
    cells.append(
        f'<text x="{x0}" y="{y0 - 8}" font-family="{FONT}" font-size="15" '
        f'font-weight="700">{label}</text>'
    )
    x = x0
    for i, h in enumerate(["Number of eggs", "Frequency"]):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{header_h}" '
            f'fill="#f3f4f6" stroke="#111"/>'
            f'<text x="{x + widths[i] / 2}" y="{y0 + 21}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="12" font-weight="700">{esc(h)}</text>'
        )
        x += widths[i]
    for r, (egg, freq) in enumerate(zip(eggs, freqs)):
        y = y0 + header_h + row_h * r
        x = x0
        for i, cell in enumerate([str(egg), str(freq)]):
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" '
                f'fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i] / 2}" y="{y + 19}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="12">{esc(cell)}</text>'
            )
            x += widths[i]
    return cells


def math2_q19_frequency_tables() -> str:
    W, H = 720, 420
    tables = [
        ("A", [7, 6, 4, 6, 7], 40, 40),
        ("B", [6, 6, 6, 6, 6], 400, 40),
        ("C", [2, 7, 12, 7, 2], 40, 230),
        ("D", [0, 5, 20, 5, 0], 400, 230),
    ]
    parts: list[str] = []
    for label, freqs, x0, y0 in tables:
        parts.extend(_freq_table(x0, y0, label, freqs))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math2_q20_age_group_table() -> str:
    headers = ["", "0–9 years", "10–19 years", "20+ years", "Total"]
    rows = [
        ["Group A", "5", "19", "11", "35"],
        ["Group B", "9", "6", "20", "35"],
        ["Group C", "21", "10", "4", "35"],
        ["Total", "35", "35", "35", "105"],
    ]
    widths = [90, 100, 110, 100, 80]
    width = sum(widths) + 40
    row_h = 34
    height = 20 + row_h * (1 + len(rows)) + 16
    x0, y0 = 20, 16
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{row_h}" '
            f'fill="#f3f4f6" stroke="#111"/>'
            f'<text x="{x + widths[i] / 2}" y="{y0 + 22}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="12" font-weight="700">{esc(h)}</text>'
        )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + row_h * (r + 1)
        x = x0
        for i, cell in enumerate(row):
            weight = ' font-weight="700"' if i == 0 or r == len(rows) - 1 else ""
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" '
                f'fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i] / 2}" y="{y + 22}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="12"{weight}>{esc(cell)}</text>'
            )
            x += widths[i]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(cells)}
</svg>'''


def main() -> None:
    write("math2-q02-triangle-abc.svg", math2_q02_triangle())
    write("math2-q06-parabola.svg", math2_q06_parabola())
    write("math2-q08-fx-table.svg", math2_q08_table())
    write("math2-q17-scatter-g.svg", math2_q17_scatter())
    write("math2-q19-frequency-tables.svg", math2_q19_frequency_tables())
    write("math2-q20-age-group-table.svg", math2_q20_age_group_table())


if __name__ == "__main__":
    main()
