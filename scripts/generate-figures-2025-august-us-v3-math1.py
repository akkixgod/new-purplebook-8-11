#!/usr/bin/env python3
"""Generate Math Module 1 SVG figures for 2025-august-us-v3."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-august-us-v3/figures")
OUT.mkdir(parents=True, exist_ok=True)
FONT = "Georgia, serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def m1_q05_table() -> str:
    headers = ["x", "g(x)"]
    rows = [["1", "34"], ["2", "27"], ["3", "20"], ["4", "13"]]
    widths = [80, 100]
    row_h = 36
    width = sum(widths) + 40
    height = 16 + row_h * (1 + len(rows)) + 16
    x0, y0 = 20, 16
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        italic = ' font-style="italic"' if h in {"x", "y"} else ""
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{row_h}" fill="#f3f4f6" stroke="#111"/>'
            f'<text x="{x + widths[i] / 2}" y="{y0 + 24}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="13" font-weight="700"{italic}>{h}</text>'
        )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + row_h * (r + 1)
        x = x0
        for i, cell in enumerate(row):
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i] / 2}" y="{y + 24}" text-anchor="middle" font-family="{FONT}" '
                f'font-size="12">{cell}</text>'
            )
            x += widths[i]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(cells)}
</svg>'''


def m1_q14_lines() -> str:
    W, H = 520, 420
    pad_l, pad_r, pad_t, pad_b = 48, 36, 28, 40
    plot_w, plot_h = W - pad_l - pad_r, H - pad_t - pad_b
    xmin, xmax, ymin, ymax = -7, 11, -7, 10

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = []
    for x in range(xmin, xmax + 1):
        parts.append(
            f'<line x1="{sx(x):.1f}" y1="{pad_t}" x2="{sx(x):.1f}" y2="{pad_t + plot_h}" stroke="#eee"/>'
        )
        if x % 2 == 0 and x != 0:
            parts.append(
                f'<text x="{sx(x):.1f}" y="{pad_t + plot_h + 16}" text-anchor="middle" '
                f'font-family="Arial" font-size="11">{x}</text>'
            )
    for y in range(ymin, ymax + 1):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(y):.1f}" x2="{pad_l + plot_w}" y2="{sy(y):.1f}" stroke="#eee"/>'
        )
        if y % 2 == 0 and y != 0:
            parts.append(
                f'<text x="{pad_l - 8}" y="{sy(y) + 4:.1f}" text-anchor="end" '
                f'font-family="Arial" font-size="11">{y}</text>'
            )

    # Shade region below both lines: sample x, take min of the two lines down to ymin
    shade_pts: list[str] = []
    xs = [i / 10 for i in range(int(xmin * 10), int(xmax * 10) + 1)]
    for x in xs:
        y_top = min(-3 * x + 5, x - 3)
        if y_top > ymin:
            shade_pts.append(f"{sx(x):.1f},{sy(y_top):.1f}")
    # close along bottom
    shade_pts.append(f"{sx(xmax):.1f},{sy(ymin):.1f}")
    shade_pts.append(f"{sx(xmin):.1f},{sy(ymin):.1f}")
    parts.append(
        f'<polygon points="{" ".join(shade_pts)}" fill="#d1d5db" fill-opacity="0.55" stroke="none"/>'
    )

    # axes
    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0):.1f}" x2="{pad_l + plot_w}" y2="{sy(0):.1f}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{sx(0):.1f}" y1="{pad_t}" x2="{sx(0):.1f}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<text x="{sx(0) + 10:.1f}" y="{sy(0) + 14:.1f}" font-family="Arial" font-size="12">O</text>'
        f'<text x="{pad_l + plot_w + 6}" y="{sy(0) + 4:.1f}" font-family="{FONT}" font-size="14" font-style="italic">x</text>'
        f'<text x="{sx(0) + 8:.1f}" y="{pad_t + 12}" font-family="{FONT}" font-size="14" font-style="italic">y</text>'
    )

    # line y = -3x+5 from x where y in range
    def clip_line(f, x0, x1, steps=80):
        pts = []
        for i in range(steps + 1):
            x = x0 + (x1 - x0) * i / steps
            y = f(x)
            if ymin - 0.5 <= y <= ymax + 0.5:
                pts.append(f"{sx(x):.1f},{sy(y):.1f}")
        return " ".join(pts)

    parts.append(
        f'<polyline points="{clip_line(lambda x: -3 * x + 5, xmin, xmax)}" fill="none" stroke="#111" stroke-width="2"/>'
        f'<polyline points="{clip_line(lambda x: x - 3, xmin, xmax)}" fill="none" stroke="#111" stroke-width="2"/>'
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def m1_q18_scatter() -> str:
    W, H = 480, 400
    pad_l, pad_r, pad_t, pad_b = 48, 36, 28, 40
    plot_w, plot_h = W - pad_l - pad_r, H - pad_t - pad_b
    xmin, xmax, ymin, ymax = 0, 10, 0, 60

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = []
    for x in range(0, 11):
        parts.append(
            f'<line x1="{sx(x):.1f}" y1="{pad_t}" x2="{sx(x):.1f}" y2="{pad_t + plot_h}" stroke="#eee"/>'
        )
        if x > 0:
            parts.append(
                f'<text x="{sx(x):.1f}" y="{pad_t + plot_h + 16}" text-anchor="middle" '
                f'font-family="Arial" font-size="11">{x}</text>'
            )
    for y in range(0, 61, 10):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(y):.1f}" x2="{pad_l + plot_w}" y2="{sy(y):.1f}" stroke="#eee"/>'
        )
        if y > 0:
            parts.append(
                f'<text x="{pad_l - 8}" y="{sy(y) + 4:.1f}" text-anchor="end" '
                f'font-family="Arial" font-size="11">{y}</text>'
            )

    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0):.1f}" x2="{pad_l + plot_w}" y2="{sy(0):.1f}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{sx(0):.1f}" y1="{pad_t}" x2="{sx(0):.1f}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<text x="{sx(0) + 8:.1f}" y="{sy(0) + 14:.1f}" font-family="Arial" font-size="12">O</text>'
        f'<text x="{pad_l + plot_w + 6}" y="{sy(0) + 4:.1f}" font-family="{FONT}" font-size="14" font-style="italic">x</text>'
        f'<text x="{sx(0) + 8:.1f}" y="{pad_t + 12}" font-family="{FONT}" font-size="14" font-style="italic">y</text>'
    )

    points = [(2, 12), (3, 22), (4, 28), (5, 41), (6, 46)]
    for x, y in points:
        parts.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="4.5" fill="#111"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def m1_q21_exp() -> str:
    W, H = 480, 400
    pad_l, pad_r, pad_t, pad_b = 48, 36, 28, 40
    plot_w, plot_h = W - pad_l - pad_r, H - pad_t - pad_b
    xmin, xmax, ymin, ymax = -4, 4, -6, 10

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = []
    for x in range(xmin, xmax + 1):
        parts.append(
            f'<line x1="{sx(x):.1f}" y1="{pad_t}" x2="{sx(x):.1f}" y2="{pad_t + plot_h}" stroke="#eee"/>'
        )
        if x % 2 == 0 and x != 0:
            parts.append(
                f'<text x="{sx(x):.1f}" y="{pad_t + plot_h + 16}" text-anchor="middle" '
                f'font-family="Arial" font-size="11">{x}</text>'
            )
    for y in range(ymin, ymax + 1):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(y):.1f}" x2="{pad_l + plot_w}" y2="{sy(y):.1f}" stroke="#eee"/>'
        )
        if y % 2 == 0 and y != 0:
            parts.append(
                f'<text x="{pad_l - 8}" y="{sy(y) + 4:.1f}" text-anchor="end" '
                f'font-family="Arial" font-size="11">{y}</text>'
            )

    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0):.1f}" x2="{pad_l + plot_w}" y2="{sy(0):.1f}" stroke="#111" stroke-width="1.5"/>'
        f'<line x1="{sx(0):.1f}" y1="{pad_t}" x2="{sx(0):.1f}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
        f'<text x="{sx(0) + 8:.1f}" y="{sy(0) + 14:.1f}" font-family="Arial" font-size="12">O</text>'
        f'<text x="{pad_l + plot_w + 6}" y="{sy(0) + 4:.1f}" font-family="{FONT}" font-size="14" font-style="italic">x</text>'
        f'<text x="{sx(0) + 8:.1f}" y="{pad_t + 12}" font-family="{FONT}" font-size="14" font-style="italic">y</text>'
    )

    # y = 9^x - 3
    curve: list[str] = []
    for i in range(0, 201):
        x = xmin + (xmax - xmin) * i / 200
        y = 9**x - 3
        if ymin - 0.5 <= y <= ymax + 0.5:
            curve.append(f"{sx(x):.1f},{sy(y):.1f}")
    parts.append(
        f'<polyline points="{" ".join(curve)}" fill="none" stroke="#111" stroke-width="2.2"/>'
    )
    for x, y in [(0, -2), (1, 6)]:
        parts.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="4.5" fill="#111"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def main() -> None:
    write("m1-q05.svg", m1_q05_table())
    write("m1-q14.svg", m1_q14_lines())
    write("m1-q18.svg", m1_q18_scatter())
    write("m1-q21.svg", m1_q21_exp())


if __name__ == "__main__":
    main()
