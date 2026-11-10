#!/usr/bin/env python3
"""Clean SVGs for 2025 Nov Int-B Math Module 1 figures."""

from pathlib import Path

OUT = Path("public/mocks/2025-nov-int-b/figures")
OUT.mkdir(parents=True, exist_ok=True)
FONT = 'font-family="Georgia, serif"'


def write(name: str, body: str) -> None:
    path = OUT / name
    path.write_text(body.strip() + "\n", encoding="utf-8")
    print("wrote", path.name)


def q05() -> None:
    tables = [
        ("A", [("0", "55"), ("2", "53"), ("4", "51")]),
        ("B", [("0", "53"), ("2", "55"), ("4", "51")]),
        ("C", [("0", "51"), ("2", "55"), ("4", "53")]),
        ("D", [("0", "51"), ("2", "53"), ("4", "55")]),
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="280" height="720" viewBox="0 0 280 720">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for i, (letter, rows) in enumerate(tables):
        top = 16 + i * 176
        parts.append(
            f'<circle cx="28" cy="{top + 68}" r="13" fill="none" stroke="#111" stroke-width="1.5"/>'
        )
        parts.append(
            f'<text x="28" y="{top + 73}" text-anchor="middle" font-family="Arial, sans-serif" font-size="15">{letter}</text>'
        )
        # header
        parts.append(
            f'<rect x="56" y="{top}" width="90" height="34" fill="#f3f4f6" stroke="#111"/>'
        )
        parts.append(
            f'<text x="101" y="{top + 23}" text-anchor="middle" font-family="Times New Roman, Times, serif" font-size="18" font-style="italic" font-weight="700">r</text>'
        )
        parts.append(
            f'<rect x="146" y="{top}" width="90" height="34" fill="#f3f4f6" stroke="#111"/>'
        )
        parts.append(
            f'<text x="191" y="{top + 23}" text-anchor="middle" font-family="Times New Roman, Times, serif" font-size="18" font-style="italic" font-weight="700">g</text>'
        )
        for j, (rv, gv) in enumerate(rows):
            y = top + 34 + j * 34
            parts.append(f'<rect x="56" y="{y}" width="90" height="34" fill="#fff" stroke="#111"/>')
            parts.append(
                f'<text x="101" y="{y + 23}" text-anchor="middle" {FONT} font-size="16">{rv}</text>'
            )
            parts.append(f'<rect x="146" y="{y}" width="90" height="34" fill="#fff" stroke="#111"/>')
            parts.append(
                f'<text x="191" y="{y + 23}" text-anchor="middle" {FONT} font-size="16">{gv}</text>'
            )
    parts.append("</svg>")
    write("math1-q05-rg-tables.svg", "\n".join(parts))


def q06() -> None:
    # Square cells: 1 x-unit = 2 y-units = 40 px. y from 0 to 14, x from 0 to 7.
    ox, oy = 78, 332
    sx, sy = 40, 20
    pts = [
        (1, 2.4),
        (1.2, 2.7),
        (1.7, 2.6),
        (2, 4),
        (2.4, 5.6),
        (3, 4),
        (3, 5.8),
        (3, 6.8),
        (5, 7.8),
        (5.3, 10.6),
        (5.4, 9.9),
        (6, 12),
    ]
    w, h = 430, 430
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for xv in range(0, 8):
        x = ox + xv * sx
        parts.append(
            f'<line x1="{x}" y1="{oy - 14 * sy}" x2="{x}" y2="{oy}" stroke="#d5d8de" stroke-width="1"/>'
        )
    for yv in range(0, 15, 2):
        y = oy - yv * sy
        parts.append(
            f'<line x1="{ox}" y1="{y}" x2="{ox + 7 * sx}" y2="{y}" stroke="#d5d8de" stroke-width="1"/>'
        )
    parts.append(
        f'<line x1="{ox}" y1="{oy}" x2="{ox + 7 * sx + 16}" y2="{oy}" stroke="#111" stroke-width="1.6"/>'
    )
    parts.append(
        f'<polygon points="{ox + 7 * sx + 22},{oy} {ox + 7 * sx + 12},{oy - 4} {ox + 7 * sx + 12},{oy + 4}" fill="#111"/>'
    )
    parts.append(
        f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy - 14 * sy - 16}" stroke="#111" stroke-width="1.6"/>'
    )
    parts.append(
        f'<polygon points="{ox},{oy - 14 * sy - 22} {ox - 4},{oy - 14 * sy - 12} {ox + 4},{oy - 14 * sy - 12}" fill="#111"/>'
    )
    parts.append(
        f'<text x="{ox + 7 * sx + 28}" y="{oy + 5}" {FONT} font-size="16" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{ox + 8}" y="{oy - 14 * sy - 26}" {FONT} font-size="16" font-style="italic">y</text>'
    )
    parts.append(
        f'<text x="{ox - 14}" y="{oy + 5}" {FONT} font-size="14" font-style="italic">O</text>'
    )
    for xv in range(1, 8):
        x = ox + xv * sx
        parts.append(f'<line x1="{x}" y1="{oy - 4}" x2="{x}" y2="{oy + 4}" stroke="#111" stroke-width="1.2"/>')
        parts.append(
            f'<text x="{x}" y="{oy + 20}" text-anchor="middle" {FONT} font-size="13">{xv}</text>'
        )
    for yv in range(2, 15, 2):
        y = oy - yv * sy
        parts.append(f'<line x1="{ox - 4}" y1="{y}" x2="{ox + 4}" y2="{y}" stroke="#111" stroke-width="1.2"/>')
        parts.append(
            f'<text x="{ox - 10}" y="{y + 4}" text-anchor="end" {FONT} font-size="13">{yv}</text>'
        )
    for xv, yv in pts:
        cx = ox + xv * sx
        cy = oy - yv * sy
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="#111"/>')
    parts.append(
        f'<text x="22" y="186" text-anchor="middle" {FONT} font-size="13" transform="rotate(-90 22 186)">Annual sales (in millions of dollars)</text>'
    )
    parts.append(
        f'<text x="{ox + 3.5 * sx}" y="{oy + 48}" text-anchor="middle" {FONT} font-size="13">Square footage of store</text>'
    )
    parts.append(
        f'<text x="{ox + 3.5 * sx}" y="{oy + 66}" text-anchor="middle" {FONT} font-size="12">(in thousands of square feet)</text>'
    )
    parts.append("</svg>")
    write("math1-q06-scatterplot.svg", "\n".join(parts))


def q09() -> None:
    rows = [
        ("Beef", "13", False),
        ("Chicken", "20", False),
        ("Fish", "8", False),
        ("Vegetarian", "9", False),
        ("Total", "50", True),
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="460" height="280" viewBox="0 0 460 280">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<rect x="20" y="16" width="250" height="42" fill="#f3f4f6" stroke="#111"/>',
        f'<text x="145" y="43" text-anchor="middle" {FONT} font-size="16" font-weight="700">Type of entree</text>',
        '<rect x="270" y="16" width="170" height="42" fill="#f3f4f6" stroke="#111"/>',
        f'<text x="355" y="43" text-anchor="middle" {FONT} font-size="16" font-weight="700">Number of people</text>',
    ]
    for i, (name, num, bold) in enumerate(rows):
        y = 58 + i * 40
        weight = ' font-weight="700"' if bold else ""
        parts.append(f'<rect x="20" y="{y}" width="250" height="40" fill="#fff" stroke="#111"/>')
        anchor = "middle" if bold else "start"
        tx = 145 if bold else 36
        parts.append(
            f'<text x="{tx}" y="{y + 26}" text-anchor="{anchor}" {FONT} font-size="16"{weight}>{name}</text>'
        )
        parts.append(f'<rect x="270" y="{y}" width="170" height="40" fill="#fff" stroke="#111"/>')
        parts.append(
            f'<text x="355" y="{y + 26}" text-anchor="middle" {FONT} font-size="16"{weight}>{num}</text>'
        )
    parts.append("</svg>")
    write("math1-q09-entree-table.svg", "\n".join(parts))


def q10() -> None:
    write(
        "math1-q10-parallel-lines.svg",
        f"""
<svg xmlns="http://www.w3.org/2000/svg" width="480" height="340" viewBox="0 0 480 340">
  <rect width="100%" height="100%" fill="#fff"/>
  <line x1="70" y1="96" x2="400" y2="96" stroke="#111" stroke-width="2"/>
  <line x1="70" y1="210" x2="430" y2="210" stroke="#111" stroke-width="2"/>
  <line x1="118" y1="28" x2="292" y2="312" stroke="#111" stroke-width="2"/>
  <text x="96" y="40" {FONT} font-size="18" font-style="italic">t</text>
  <text x="408" y="102" {FONT} font-size="18" font-style="italic">ℓ</text>
  <text x="438" y="216" {FONT} font-size="18" font-style="italic">k</text>
  <text x="214" y="84" {FONT} font-size="16" font-style="italic">x<tspan font-style="normal">°</tspan></text>
  <text x="168" y="198" {FONT} font-size="16" font-style="italic">y<tspan font-style="normal">°</tspan></text>
  <text x="240" y="332" text-anchor="middle" {FONT} font-size="13">Note: Figure not drawn to scale.</text>
</svg>
""",
    )


def q13() -> None:
    # Number line 32 to 50. Whiskers 34 and 49, box 36 to 46, median 41.
    x0, y_line = 48, 78
    scale = 22  # px per cm

    def X(v: float) -> float:
        return x0 + (v - 32) * scale

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="500" height="170" viewBox="0 0 500 170">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<line x1="{X(32):.0f}" y1="{y_line}" x2="{X(50):.0f}" y2="{y_line}" stroke="#111" stroke-width="1.4"/>',
    ]
    for v in range(32, 51, 2):
        x = X(v)
        parts.append(f'<line x1="{x:.0f}" y1="{y_line}" x2="{x:.0f}" y2="{y_line + 10}" stroke="#111" stroke-width="1.2"/>')
        parts.append(
            f'<text x="{x:.0f}" y="{y_line + 28}" text-anchor="middle" {FONT} font-size="14">{v}</text>'
        )
    # whiskers and box, sitting above the axis
    yb = 36
    parts.append(f'<line x1="{X(34):.0f}" y1="{yb + 16}" x2="{X(36):.0f}" y2="{yb + 16}" stroke="#111" stroke-width="1.6"/>')
    parts.append(f'<line x1="{X(46):.0f}" y1="{yb + 16}" x2="{X(49):.0f}" y2="{yb + 16}" stroke="#111" stroke-width="1.6"/>')
    parts.append(f'<line x1="{X(34):.0f}" y1="{yb + 8}" x2="{X(34):.0f}" y2="{yb + 24}" stroke="#111" stroke-width="1.6"/>')
    parts.append(f'<line x1="{X(49):.0f}" y1="{yb + 8}" x2="{X(49):.0f}" y2="{yb + 24}" stroke="#111" stroke-width="1.6"/>')
    parts.append(
        f'<rect x="{X(36):.0f}" y="{yb}" width="{X(46) - X(36):.0f}" height="32" fill="#fff" stroke="#111" stroke-width="1.6"/>'
    )
    parts.append(
        f'<line x1="{X(41):.0f}" y1="{yb}" x2="{X(41):.0f}" y2="{yb + 32}" stroke="#111" stroke-width="1.6"/>'
    )
    parts.append(
        f'<text x="{X(41):.0f}" y="156" text-anchor="middle" {FONT} font-size="15">Shoal bass length (cm)</text>'
    )
    parts.append("</svg>")
    write("math1-q13-boxplot.svg", "\n".join(parts))


def q14() -> None:
    write(
        "math1-q14-triangle.svg",
        f"""
<svg xmlns="http://www.w3.org/2000/svg" width="460" height="240" viewBox="0 0 460 240">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="48,168 168,48 400,168" fill="none" stroke="#111" stroke-width="2"/>
  <line x1="168" y1="48" x2="168" y2="168" stroke="#111" stroke-width="1.6" stroke-dasharray="5 4"/>
  <polyline points="168,156 180,156 180,168" fill="none" stroke="#111" stroke-width="1.4"/>
  <text x="32" y="186" {FONT} font-size="16" font-style="italic">A</text>
  <text x="168" y="38" text-anchor="middle" {FONT} font-size="16" font-style="italic">B</text>
  <text x="408" y="186" {FONT} font-size="16" font-style="italic">C</text>
  <text x="148" y="116" {FONT} font-size="16" font-style="italic">h</text>
  <text x="224" y="206" text-anchor="middle" {FONT} font-size="14">10 cm</text>
  <text x="230" y="224" text-anchor="middle" {FONT} font-size="13">Note: Figure not drawn to scale.</text>
</svg>
""",
    )


def q17() -> None:
    # y = (x - 4) / (x + 6), window [-8, 8] x [-8, 8]. Traced from the page graph.
    xmin, xmax, ymin, ymax = -8, 8, -8, 8
    k = 26
    ml, mt, mr, mb = 46, 28, 36, 36
    w = ml + mr + (xmax - xmin) * k
    h = mt + mb + (ymax - ymin) * k

    def px(x: float) -> float:
        return ml + (x - xmin) * k

    def py(y: float) -> float:
        return mt + (ymax - y) * k

    def f(x: float) -> float:
        # Vertical asymptote x = -6, x-intercept x = 4. Scale matches the left branch near (-8, 4).
        return (2 / 3) * (x - 4) / (x + 6)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for gx in range(xmin, xmax + 1):
        parts.append(
            f'<line x1="{px(gx):.1f}" y1="{py(ymax):.1f}" x2="{px(gx):.1f}" y2="{py(ymin):.1f}" stroke="#d5d8de" stroke-width="1"/>'
        )
    for gy in range(ymin, ymax + 1):
        parts.append(
            f'<line x1="{px(xmin):.1f}" y1="{py(gy):.1f}" x2="{px(xmax):.1f}" y2="{py(gy):.1f}" stroke="#d5d8de" stroke-width="1"/>'
        )
    parts.append(
        f'<line x1="{px(xmin):.1f}" y1="{py(0):.1f}" x2="{px(xmax) + 10:.1f}" y2="{py(0):.1f}" stroke="#111" stroke-width="1.6"/>'
    )
    parts.append(
        f'<polygon points="{px(xmax) + 16:.1f},{py(0):.1f} {px(xmax) + 8:.1f},{py(0) - 4:.1f} {px(xmax) + 8:.1f},{py(0) + 4:.1f}" fill="#111"/>'
    )
    parts.append(
        f'<text x="{px(xmax) + 20:.1f}" y="{py(0) + 5:.1f}" {FONT} font-size="15" font-style="italic">x</text>'
    )
    parts.append(
        f'<line x1="{px(0):.1f}" y1="{py(ymin):.1f}" x2="{px(0):.1f}" y2="{py(ymax) - 10:.1f}" stroke="#111" stroke-width="1.6"/>'
    )
    parts.append(
        f'<polygon points="{px(0):.1f},{py(ymax) - 16:.1f} {px(0) - 4:.1f},{py(ymax) - 8:.1f} {px(0) + 4:.1f},{py(ymax) - 8:.1f}" fill="#111"/>'
    )
    parts.append(
        f'<text x="{px(0) + 8:.1f}" y="{py(ymax) - 12:.1f}" {FONT} font-size="15" font-style="italic">y</text>'
    )
    for v in (-8, -6, -4, -2, 2, 4, 6, 8):
        parts.append(
            f'<line x1="{px(v):.1f}" y1="{py(0) - 4:.1f}" x2="{px(v):.1f}" y2="{py(0) + 4:.1f}" stroke="#111" stroke-width="1.2"/>'
        )
        parts.append(
            f'<text x="{px(v):.1f}" y="{py(0) + 18:.1f}" text-anchor="middle" {FONT} font-size="13">{v}</text>'
        )
        parts.append(
            f'<line x1="{px(0) - 4:.1f}" y1="{py(v):.1f}" x2="{px(0) + 4:.1f}" y2="{py(v):.1f}" stroke="#111" stroke-width="1.2"/>'
        )
        parts.append(
            f'<text x="{px(0) - 8:.1f}" y="{py(v) + 4:.1f}" text-anchor="end" {FONT} font-size="13">{v}</text>'
        )
    parts.append(
        f'<text x="{px(0) - 16:.1f}" y="{py(0) + 16:.1f}" {FONT} font-size="14" font-style="italic">O</text>'
    )

    def clip_y(x0: float, y0: float, x1: float, y1: float) -> tuple[float, float]:
        """Return the point on the segment where y hits the window edge."""
        if y1 > ymax:
            edge = ymax
        elif y1 < ymin:
            edge = ymin
        else:
            edge = y1
        t = (edge - y0) / (y1 - y0)
        return x0 + t * (x1 - x0), edge

    def branch(x_start: float, x_end: float, step: float) -> None:
        pts: list[tuple[float, float]] = []
        x = x_start
        prev: tuple[float, float] | None = None
        while x <= x_end + 1e-9:
            y = f(x)
            inside = ymin <= y <= ymax
            if inside:
                if prev is not None and not (ymin <= prev[1] <= ymax):
                    pts.append(clip_y(prev[0], prev[1], x, y))
                pts.append((x, y))
            elif prev is not None and ymin <= prev[1] <= ymax:
                pts.append(clip_y(prev[0], prev[1], x, y))
            prev = (x, y)
            x += step
        if len(pts) < 2:
            return
        dcmd = " ".join(f"{px(xv):.1f},{py(yv):.1f}" for xv, yv in pts)
        parts.append(
            f'<polyline points="{dcmd}" fill="none" stroke="#111" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
        )

    branch(-8, -6.15, 0.02)
    branch(-5.85, 8, 0.04)
    parts.append("</svg>")
    write("math1-q17-rational-graph.svg", "\n".join(parts))


def main() -> None:
    q05()
    q06()
    q09()
    q10()
    q13()
    q14()
    q17()


if __name__ == "__main__":
    main()
