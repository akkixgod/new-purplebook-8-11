#!/usr/bin/env python3
"""Clean SVGs for 2025 Nov Int-C Math Module 1 figures."""

from pathlib import Path

OUT = Path("public/mocks/2025-nov-int-c/figures")
OUT.mkdir(parents=True, exist_ok=True)
FONT = 'font-family="Times New Roman, Times, serif"'


def write(name: str, body: str) -> None:
    path = OUT / name
    path.write_text(body.strip() + "\n", encoding="utf-8")
    print("wrote", path.name)


def q05() -> None:
    # Measured from page-37: 12 points. Cells are square (1 x-unit = 2 y-units).
    ox, oy = 78, 360
    sx, sy = 44, 22  # px per x-unit, px per y-unit
    pts = [
        (1, 2.3),
        (1.3, 2.6),
        (1.7, 2.5),
        (2, 4),
        (2.4, 5.6),
        (2.9, 5.7),
        (3, 4),
        (3, 7.1),
        (5, 7.7),
        (5.2, 10.5),
        (5.4, 9.4),
        (6, 12),
    ]
    w, h = 460, 460
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
        f'<text x="{ox - 16}" y="{oy + 5}" {FONT} font-size="14" font-style="italic">O</text>'
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
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.6" fill="#111"/>')
    parts.append(
        f'<text x="22" y="200" text-anchor="middle" {FONT} font-size="13" transform="rotate(-90 22 200)">Annual sales (in millions of dollars)</text>'
    )
    parts.append(
        f'<text x="{ox + 3.5 * sx}" y="{oy + 48}" text-anchor="middle" {FONT} font-size="13">Square footage of store</text>'
    )
    parts.append(
        f'<text x="{ox + 3.5 * sx}" y="{oy + 66}" text-anchor="middle" {FONT} font-size="12">(in thousands of square feet)</text>'
    )
    parts.append("</svg>")
    write("math1-q05-scatterplot.svg", "\n".join(parts))


def q10() -> None:
    # Right angle at the lower right. 58° is at the top, between sides b and c,
    # so the angle opposite side b is 32°.
    write(
        "math1-q10-triangle.svg",
        f"""
<svg xmlns="http://www.w3.org/2000/svg" width="520" height="300" viewBox="0 0 520 300">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="48,230 400,230 400,42" fill="none" stroke="#111" stroke-width="2"/>
  <polyline points="384,230 384,214 400,214" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="214" y="256" text-anchor="middle" {FONT} font-size="20" font-style="italic">a</text>
  <text x="418" y="142" {FONT} font-size="20" font-style="italic">b</text>
  <text x="188" y="128" {FONT} font-size="20" font-style="italic">c</text>
  <text x="362" y="68" {FONT} font-size="16">58°</text>
  <text x="224" y="284" text-anchor="middle" {FONT} font-size="13">Note: Figure not drawn to scale.</text>
</svg>
""",
    )


def q11() -> None:
    # Transversal falls down to the right. x° is above ℓ and right of t;
    # y° is above k and left of t. Those angles are supplementary.
    write(
        "math1-q11-parallel-lines.svg",
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
    # Line through (0, 50) and (10, 210): slope 16, intercept 50.
    ox, oy = 78, 392
    sx, sy = 32, 32  # 1 x-unit and 50 y-units
    w, h = 500, 470
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for xv in range(0, 11):
        x = ox + xv * sx
        parts.append(
            f'<line x1="{x}" y1="{oy - 10 * sy}" x2="{x}" y2="{oy}" stroke="#d5d8de" stroke-width="1"/>'
        )
    for i in range(0, 11):
        y = oy - i * sy
        parts.append(
            f'<line x1="{ox}" y1="{y}" x2="{ox + 10 * sx}" y2="{y}" stroke="#d5d8de" stroke-width="1"/>'
        )
    parts.append(
        f'<line x1="{ox}" y1="{oy}" x2="{ox + 10 * sx + 18}" y2="{oy}" stroke="#111" stroke-width="1.6"/>'
    )
    parts.append(
        f'<polygon points="{ox + 10 * sx + 24},{oy} {ox + 10 * sx + 14},{oy - 4} {ox + 10 * sx + 14},{oy + 4}" fill="#111"/>'
    )
    parts.append(
        f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy - 10 * sy - 16}" stroke="#111" stroke-width="1.6"/>'
    )
    parts.append(
        f'<polygon points="{ox},{oy - 10 * sy - 22} {ox - 4},{oy - 10 * sy - 12} {ox + 4},{oy - 10 * sy - 12}" fill="#111"/>'
    )
    parts.append(
        f'<text x="{ox + 10 * sx + 30}" y="{oy + 5}" {FONT} font-size="16" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{ox + 8}" y="{oy - 10 * sy - 26}" {FONT} font-size="16" font-style="italic">y</text>'
    )
    parts.append(
        f'<text x="{ox - 16}" y="{oy + 16}" {FONT} font-size="14" font-style="italic">O</text>'
    )
    for xv in range(1, 11):
        x = ox + xv * sx
        parts.append(f'<line x1="{x}" y1="{oy - 4}" x2="{x}" y2="{oy + 4}" stroke="#111" stroke-width="1.2"/>')
        parts.append(
            f'<text x="{x}" y="{oy + 20}" text-anchor="middle" {FONT} font-size="13">{xv}</text>'
        )
    for i, label in enumerate(range(50, 501, 50)):
        y = oy - (i + 1) * sy
        parts.append(f'<line x1="{ox - 4}" y1="{y}" x2="{ox + 4}" y2="{y}" stroke="#111" stroke-width="1.2"/>')
        parts.append(
            f'<text x="{ox - 10}" y="{y + 4}" text-anchor="end" {FONT} font-size="13">{label}</text>'
        )
    x0, y0 = ox, oy - sy  # (0, 50)
    x1, y1 = ox + 10 * sx, oy - 210 / 50 * sy  # (10, 210)
    parts.append(
        f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#111" stroke-width="2.4" stroke-linecap="round"/>'
    )
    parts.append("</svg>")
    write("math1-q13-cost-graph.svg", "\n".join(parts))


def main() -> None:
    q05()
    q10()
    q11()
    q13()


if __name__ == "__main__":
    main()
