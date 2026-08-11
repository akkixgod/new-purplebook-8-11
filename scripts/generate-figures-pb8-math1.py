#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for PurpleBook test 8 Math Module 1."""

from __future__ import annotations

import math
from pathlib import Path

OUT = Path("public/mocks/purplebook-test-8/figures")
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
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{hh}" fill="#fff" stroke="#111"/>'
        )
        if "|" in h:
            lines = h.split("|")
            line_h = 14
            start_y = y0 + (hh - line_h * (len(lines) - 1)) / 2 - 2
            for li, line in enumerate(lines):
                cells.append(
                    f'<text x="{x + widths[i] / 2}" y="{start_y + li * line_h}" text-anchor="middle" '
                    f'font-family="{FONT}" font-size="{header_font}" font-weight="700">{line}</text>'
                )
        else:
            cells.append(
                f'<text x="{x + widths[i] / 2}" y="{y0 + hh / 2 + 4}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="{header_font}" font-weight="700">{h}</text>'
            )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + hh + rh * r
        x = x0
        for i, cell in enumerate(row):
            weight = ' font-weight="700"' if (row_labels_bold and i == 0) else ""
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{rh}" fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i] / 2}" y="{y + rh / 2 + 4}" text-anchor="middle" '
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
            ["Less than 45 years old", "15", "15", "30"],
            ["At least 45 years old", "20", "85", "105"],
            ["Total", "35", "100", "135"],
        ],
        [180, 120, 120, 80],
        header_font=12,
        font_size=13,
        header_h=52,
        row_h=42,
        row_labels_bold=True,
    )


def math1_q05_scatter() -> str:
    """Scatterplot with positive line of best fit y ≈ 1.1x."""
    W, H = 420, 420
    pad_l, pad_r, pad_t, pad_b = 40, 36, 28, 40
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmax = ymax = 6.0

    def sx(x: float) -> float:
        return pad_l + (x / xmax) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / ymax) * plot_h

    points = [
        (0.5, 0.7),
        (1.0, 1.4),
        (1.8, 1.7),
        (2.3, 2.6),
        (2.9, 3.0),
        (3.4, 4.0),
        (4.1, 4.3),
        (4.7, 5.4),
        (5.2, 5.5),
    ]
    slope = 1.1
    parts: list[str] = []
    for i in range(0, 7):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" stroke="#e5e7eb"/>'
        )
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(i)}" x2="{pad_l + plot_w}" y2="{sy(i)}" stroke="#e5e7eb"/>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    for i in range(0, 7):
        parts.append(
            f'<text x="{sx(i)}" y="{pad_t + plot_h + 18}" text-anchor="middle" '
            f'font-family="Arial" font-size="12">{i}</text>'
        )
        parts.append(
            f'<text x="{pad_l - 8}" y="{sy(i) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="12">{i}</text>'
        )
    # line of best fit from (0,0) through (6, 6.6) clipped to plot
    x2 = min(6.0, ymax / slope)
    parts.append(
        f'<line x1="{sx(0)}" y1="{sy(0)}" x2="{sx(x2)}" y2="{sy(slope * x2)}" '
        f'stroke="#111" stroke-width="2"/>'
    )
    for px, py in points:
        parts.append(f'<circle cx="{sx(px)}" cy="{sy(py)}" r="4" fill="#111"/>')
    parts.append(
        f'<text x="{pad_l + plot_w + 8}" y="{pad_t + plot_h + 4}" font-family="Arial" '
        f'font-size="14" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{pad_l - 4}" y="{pad_t - 8}" font-family="Arial" '
        f'font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q09_height_table() -> str:
    return table_svg(
        ["Height", "Frequency"],
        [
            ["0 to 100", "8"],
            ["101 to 200", "6"],
            ["201 to 300", "5"],
            ["301 to 400", "4"],
            ["401 to 500", "2"],
        ],
        [140, 110],
        font_size=14,
        header_font=14,
    )


def math1_q11_scatter() -> str:
    """Scatterplot with negative line of best fit, slope ≈ −1.1."""
    W, H = 520, 440
    pad_l, pad_r, pad_t, pad_b = 44, 40, 28, 44
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmax, ymax = 16.0, 14.0

    def sx(x: float) -> float:
        return pad_l + (x / xmax) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / ymax) * plot_h

    points = [
        (2.0, 12.0),
        (3.2, 10.2),
        (4.5, 9.2),
        (5.5, 10.8),
        (6.0, 7.2),
        (7.0, 8.8),
        (7.5, 6.2),
        (9.0, 5.0),
        (10.0, 2.5),
        (11.0, 3.8),
    ]
    # y = 13.2 − 1.1x
    intercept, slope = 13.2, -1.1
    parts: list[str] = []
    for i in range(0, 17):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" stroke="#e5e7eb"/>'
        )
    for j in range(0, 15):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l + plot_w}" y2="{sy(j)}" stroke="#e5e7eb"/>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    for i in range(0, 17, 2):
        parts.append(
            f'<text x="{sx(i)}" y="{pad_t + plot_h + 18}" text-anchor="middle" '
            f'font-family="Arial" font-size="12">{i if i else "O"}</text>'
        )
    for j in range(2, 15, 2):
        parts.append(
            f'<text x="{pad_l - 8}" y="{sy(j) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="12">{j}</text>'
        )
    # line clipped to plot
    x_start = 0.0
    y_start = intercept
    x_end = min(xmax, (0 - intercept) / slope)  # where y=0
    y_end = intercept + slope * x_end
    if y_start > ymax:
        x_start = (ymax - intercept) / slope
        y_start = ymax
    parts.append(
        f'<line x1="{sx(x_start)}" y1="{sy(y_start)}" x2="{sx(x_end)}" y2="{sy(y_end)}" '
        f'stroke="#111" stroke-width="2"/>'
    )
    for px, py in points:
        parts.append(f'<circle cx="{sx(px)}" cy="{sy(py)}" r="4" fill="#111"/>')
    parts.append(
        f'<text x="{pad_l + plot_w + 6}" y="{pad_t + plot_h + 4}" font-family="Arial" '
        f'font-size="14" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{pad_l - 4}" y="{pad_t - 8}" font-family="Arial" '
        f'font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q15_fx_table() -> str:
    return table_svg(
        ["x", "f(x)"],
        [
            ["−37", "4"],
            ["−9", "0"],
            ["33", "6"],
        ],
        [90, 90],
        font_size=15,
        header_font=15,
    )


def math1_q16_line_k() -> str:
    """Line k through (−6, 0) and (0, −5); slope −5/6."""
    W, H = 460, 460
    pad_l, pad_r, pad_t, pad_b = 40, 36, 28, 40
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = -10.0, 2.0
    ymin, ymax = -10.0, 2.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = []
    for i in range(int(xmin), int(xmax) + 1):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" stroke="#e5e7eb"/>'
        )
    for j in range(int(ymin), int(ymax) + 1):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l + plot_w}" y2="{sy(j)}" stroke="#e5e7eb"/>'
        )
    # axes through origin
    parts.append(
        f'<line x1="{sx(xmin)}" y1="{sy(0)}" x2="{sx(xmax)}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{sy(ymin)}" x2="{sx(0)}" y2="{sy(ymax)}" stroke="#111" stroke-width="1.5"/>'
    )
    for i in range(int(xmin), int(xmax) + 1):
        if i == 0:
            continue
        parts.append(
            f'<text x="{sx(i)}" y="{sy(0) + 16}" text-anchor="middle" '
            f'font-family="Arial" font-size="11">{i}</text>'
        )
    for j in range(int(ymin), int(ymax) + 1):
        if j == 0:
            continue
        parts.append(
            f'<text x="{sx(0) - 8}" y="{sy(j) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="11">{j}</text>'
        )
    parts.append(
        f'<text x="{sx(0) - 8}" y="{sy(0) + 14}" text-anchor="end" '
        f'font-family="Arial" font-size="11">0</text>'
    )
    # line: y = (−5/6)(x + 6) = (−5/6)x − 5
    # extend across visible region
    x1, x2 = xmin, xmax
    y1 = (-5 / 6) * x1 - 5
    y2 = (-5 / 6) * x2 - 5
    # clip to y bounds roughly
    def clip_seg(xa, ya, xb, yb):
        # simple: if either end outside, adjust along line
        pts = []
        for t in [i / 200 for i in range(201)]:
            x = xa + t * (xb - xa)
            y = ya + t * (yb - ya)
            if xmin <= x <= xmax and ymin <= y <= ymax:
                pts.append((x, y))
        if not pts:
            return xa, ya, xb, yb
        return pts[0][0], pts[0][1], pts[-1][0], pts[-1][1]

    cx1, cy1, cx2, cy2 = clip_seg(x1, y1, x2, y2)
    parts.append(
        f'<line x1="{sx(cx1)}" y1="{sy(cy1)}" x2="{sx(cx2)}" y2="{sy(cy2)}" '
        f'stroke="#111" stroke-width="2.2"/>'
    )
    # label k near lower-right portion of line
    parts.append(
        f'<text x="{sx(-1.2)}" y="{sy(-6.2)}" font-family="Arial" font-size="16" '
        f'font-style="italic">k</text>'
    )
    parts.append(
        f'<text x="{sx(xmax) + 6}" y="{sy(0) + 4}" font-family="Arial" '
        f'font-size="14" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 6}" y="{sy(ymax) - 4}" font-family="Arial" '
        f'font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q17_xy_table() -> str:
    return table_svg(
        ["x", "y"],
        [
            ["k", "26"],
            ["k + 4", "14"],
            ["k + 8", "2"],
        ],
        [100, 80],
        font_size=15,
        header_font=15,
    )


def math1_q19_exponential() -> str:
    """Graph of f(x) = −2·2^x − 3; never crosses x-axis."""
    W, H = 500, 420
    pad_l, pad_r, pad_t, pad_b = 44, 36, 28, 40
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = -10.0, 10.0
    ymin, ymax = -10.0, 2.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    def f(x: float) -> float:
        return -2 * (2**x) - 3

    parts: list[str] = []
    for i in range(int(xmin), int(xmax) + 1):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" stroke="#e5e7eb"/>'
        )
    for j in range(int(ymin), int(ymax) + 1):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l + plot_w}" y2="{sy(j)}" stroke="#e5e7eb"/>'
        )
    parts.append(
        f'<line x1="{sx(xmin)}" y1="{sy(0)}" x2="{sx(xmax)}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{sy(ymin)}" x2="{sx(0)}" y2="{sy(ymax)}" stroke="#111" stroke-width="1.5"/>'
    )
    for i in range(int(xmin), int(xmax) + 1, 2):
        if i == 0:
            continue
        parts.append(
            f'<text x="{sx(i)}" y="{sy(0) + 16}" text-anchor="middle" '
            f'font-family="Arial" font-size="11">{i}</text>'
        )
    for j in range(int(ymin), int(ymax) + 1, 2):
        if j == 0:
            continue
        parts.append(
            f'<text x="{sx(0) - 8}" y="{sy(j) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="11">{j}</text>'
        )
    # curve path
    pts: list[str] = []
    for i in range(0, 401):
        x = xmin + (xmax - xmin) * i / 400
        y = f(x)
        if y < ymin - 0.5 or y > ymax + 0.5:
            if pts and pts[-1] != "M":
                pts.append("M")  # marker to break
            continue
        cmd = "M" if not pts or pts[-1] == "M" else "L"
        if pts and pts[-1] == "M":
            pts.pop()
            cmd = "M"
        pts.append(f"{cmd}{sx(x):.2f},{sy(y):.2f}")
    # clean M markers
    path_d = " ".join(p for p in pts if p != "M")
    # rebuild properly
    segments: list[list[tuple[float, float]]] = [[]]
    for i in range(0, 401):
        x = xmin + (xmax - xmin) * i / 400
        y = f(x)
        if ymin - 0.2 <= y <= ymax + 0.2:
            segments[-1].append((sx(x), sy(y)))
        elif segments[-1]:
            segments.append([])
    path_parts = []
    for seg in segments:
        if len(seg) < 2:
            continue
        d = f"M{seg[0][0]:.2f},{seg[0][1]:.2f} " + " ".join(
            f"L{p[0]:.2f},{p[1]:.2f}" for p in seg[1:]
        )
        path_parts.append(f'<path d="{d}" fill="none" stroke="#111" stroke-width="2.2"/>')
    parts.extend(path_parts)
    parts.append(
        f'<text x="{sx(xmax) + 6}" y="{sy(0) + 4}" font-family="Arial" '
        f'font-size="14" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 6}" y="{sy(ymax) - 4}" font-family="Arial" '
        f'font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math1_q22_exponential() -> str:
    """Graph of y = 7^x − 2; asymptote y=−2, through (0,−1) and (1,5); a−b=9."""
    W, H = 440, 480
    pad_l, pad_r, pad_t, pad_b = 44, 36, 28, 40
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = -4.0, 4.0
    ymin, ymax = -2.0, 10.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    def f(x: float) -> float:
        return (7**x) - 2

    parts: list[str] = []
    for i in range(int(xmin), int(xmax) + 1):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" stroke="#e5e7eb"/>'
        )
    for j in range(int(ymin), int(ymax) + 1):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l + plot_w}" y2="{sy(j)}" stroke="#e5e7eb"/>'
        )
    parts.append(
        f'<line x1="{sx(xmin)}" y1="{sy(0)}" x2="{sx(xmax)}" y2="{sy(0)}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{sy(ymin)}" x2="{sx(0)}" y2="{sy(ymax)}" stroke="#111" stroke-width="1.5"/>'
    )
    for i in [-4, -2, 2, 4]:
        parts.append(
            f'<text x="{sx(i)}" y="{sy(0) + 16}" text-anchor="middle" '
            f'font-family="Arial" font-size="12">{i}</text>'
        )
    for j in [-2, 2, 4, 6, 8, 10]:
        parts.append(
            f'<text x="{sx(0) - 8}" y="{sy(j) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="12">{j}</text>'
        )
    segments: list[list[tuple[float, float]]] = [[]]
    for i in range(0, 500):
        x = xmin + (xmax - xmin) * i / 499
        try:
            y = f(x)
        except OverflowError:
            if segments[-1]:
                segments.append([])
            continue
        if ymin - 0.15 <= y <= ymax + 0.15:
            segments[-1].append((sx(x), sy(y)))
        elif segments[-1]:
            segments.append([])
    for seg in segments:
        if len(seg) < 2:
            continue
        d = f"M{seg[0][0]:.2f},{seg[0][1]:.2f} " + " ".join(
            f"L{p[0]:.2f},{p[1]:.2f}" for p in seg[1:]
        )
        parts.append(f'<path d="{d}" fill="none" stroke="#111" stroke-width="2.2"/>')
    parts.append(
        f'<text x="{sx(xmax) + 6}" y="{sy(0) + 4}" font-family="Arial" '
        f'font-size="14" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 6}" y="{sy(ymax) - 4}" font-family="Arial" '
        f'font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def main() -> None:
    write("math1-q01-member-table.svg", math1_q01_member_table())
    write("math1-q05-scatter-best-fit.svg", math1_q05_scatter())
    write("math1-q09-height-frequency.svg", math1_q09_height_table())
    write("math1-q11-scatter-best-fit.svg", math1_q11_scatter())
    write("math1-q15-fx-table.svg", math1_q15_fx_table())
    write("math1-q16-line-k.svg", math1_q16_line_k())
    write("math1-q17-xy-table.svg", math1_q17_xy_table())
    write("math1-q19-exponential.svg", math1_q19_exponential())
    write("math1-q22-exponential.svg", math1_q22_exponential())


if __name__ == "__main__":
    main()
