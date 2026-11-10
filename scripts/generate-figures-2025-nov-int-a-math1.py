#!/usr/bin/env python3
"""Clean SVGs for 2025 Nov Int-A Math Module 1 figures."""

from pathlib import Path

OUT = Path("public/mocks/2025-nov-int-a/figures")
OUT.mkdir(parents=True, exist_ok=True)
FONT = 'font-family="Georgia, serif"'


def write(name: str, body: str) -> None:
    path = OUT / name
    path.write_text(body.strip() + "\n", encoding="utf-8")
    print("wrote", path.name)


def q02() -> None:
    write(
        "math1-q02-parallel-lines.svg",
        f"""
<svg xmlns="http://www.w3.org/2000/svg" width="460" height="320" viewBox="0 0 460 320">
  <rect width="100%" height="100%" fill="#fff"/>
  <line x1="36" y1="108" x2="400" y2="108" stroke="#111" stroke-width="2"/>
  <line x1="70" y1="214" x2="400" y2="214" stroke="#111" stroke-width="2"/>
  <line x1="78" y1="28" x2="268" y2="292" stroke="#111" stroke-width="2"/>
  <text x="62" y="36" {FONT} font-size="18" font-style="italic">t</text>
  <text x="408" y="114" {FONT} font-size="18" font-style="italic">p</text>
  <text x="408" y="220" {FONT} font-size="18" font-style="italic">r</text>
  <text x="78" y="96" {FONT} font-size="16" font-style="italic">x<tspan font-style="normal">°</tspan></text>
  <text x="168" y="138" {FONT} font-size="16">72°</text>
  <text x="230" y="304" text-anchor="middle" {FONT} font-size="13">Note: Figure not drawn to scale.</text>
</svg>
""",
    )


def q11() -> None:
    # Traced from the page graph. y = a x^3 + b x^2 + c x + d (mse ~ 0.01).
    a, b, c, d = -0.3340056154525474, -0.6507727310911494, 2.6942489745357174, -0.08916131110788506

    def f(x: float) -> float:
        return ((a * x + b) * x + c) * x + d

    xmin, xmax, ymin, ymax = -6, 6, -8, 8
    k = 26
    ml, mt, mr, mb = 46, 28, 40, 36
    w = ml + mr + (xmax - xmin) * k
    h = mt + mb + (ymax - ymin) * k

    def px(x: float) -> float:
        return ml + (x - xmin) * k

    def py(y: float) -> float:
        return mt + (ymax - y) * k

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
    # axes
    parts.append(
        f'<line x1="{px(xmin):.1f}" y1="{py(0):.1f}" x2="{px(xmax):.1f}" y2="{py(0):.1f}" stroke="#111" stroke-width="1.6"/>'
    )
    parts.append(
        f'<polygon points="{px(xmax)+9:.1f},{py(0):.1f} {px(xmax):.1f},{py(0)-4.2:.1f} {px(xmax):.1f},{py(0)+4.2:.1f}" fill="#111"/>'
    )
    parts.append(
        f'<text x="{px(xmax)+14:.1f}" y="{py(0)+5:.1f}" {FONT} font-size="15" font-style="italic">x</text>'
    )
    parts.append(
        f'<line x1="{px(0):.1f}" y1="{py(ymin):.1f}" x2="{px(0):.1f}" y2="{py(ymax):.1f}" stroke="#111" stroke-width="1.6"/>'
    )
    parts.append(
        f'<polygon points="{px(0):.1f},{py(ymax)-9:.1f} {px(0)-4.2:.1f},{py(ymax):.1f} {px(0)+4.2:.1f},{py(ymax):.1f}" fill="#111"/>'
    )
    parts.append(
        f'<text x="{px(0)+8:.1f}" y="{py(ymax)-10:.1f}" {FONT} font-size="15" font-style="italic">y</text>'
    )
    for v in (-6, -4, -2, 2, 4, 6):
        parts.append(
            f'<line x1="{px(v):.1f}" y1="{py(0)-4:.1f}" x2="{px(v):.1f}" y2="{py(0)+4:.1f}" stroke="#111" stroke-width="1.2"/>'
        )
        parts.append(
            f'<text x="{px(v):.1f}" y="{py(0)+18:.1f}" text-anchor="middle" {FONT} font-size="13">{v}</text>'
        )
    for v in (-8, -6, -4, -2, 2, 4, 6, 8):
        parts.append(
            f'<line x1="{px(0)-4:.1f}" y1="{py(v):.1f}" x2="{px(0)+4:.1f}" y2="{py(v):.1f}" stroke="#111" stroke-width="1.2"/>'
        )
        parts.append(
            f'<text x="{px(0)-8:.1f}" y="{py(v)+4:.1f}" text-anchor="end" {FONT} font-size="13">{v}</text>'
        )
    parts.append(
        f'<text x="{px(0)-12:.1f}" y="{py(0)+16:.1f}" {FONT} font-size="14" font-style="italic">O</text>'
    )
    # visible portion of the cubic, clipped to the window
    pts = []
    x = -5.2
    while x <= 3.6:
        y = f(x)
        if ymin <= y <= ymax:
            pts.append((x, y))
        x += 0.05
    # snap ends to the window border
    if pts:
        if pts[0][1] < ymax - 0.05:
            # entered from the top; walk back
            pass
        dcmd = " ".join(f"{px(x):.1f},{py(y):.1f}" for x, y in pts)
        parts.append(
            f'<polyline points="{dcmd}" fill="none" stroke="#111" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
        )
    parts.append("</svg>")
    write("math1-q11-cubic-graph.svg", "\n".join(parts))


def q14() -> None:
    write(
        "math1-q14-dilated-triangles.svg",
        f"""
<svg xmlns="http://www.w3.org/2000/svg" width="520" height="230" viewBox="0 0 520 230">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="48,150 118,62 188,150" fill="none" stroke="#111" stroke-width="2"/>
  <polygon points="230,168 360,28 490,168" fill="none" stroke="#111" stroke-width="2"/>
  <text x="36" y="170" {FONT} font-size="16" font-style="italic">A</text>
  <text x="110" y="52" text-anchor="middle" {FONT} font-size="16" font-style="italic">B</text>
  <text x="194" y="170" {FONT} font-size="16" font-style="italic">C</text>
  <text x="214" y="188" {FONT} font-size="16" font-style="italic">A′</text>
  <text x="360" y="20" text-anchor="middle" {FONT} font-size="16" font-style="italic">B′</text>
  <text x="496" y="188" {FONT} font-size="16" font-style="italic">C′</text>
  <text x="260" y="218" text-anchor="middle" {FONT} font-size="13">Note: Figures not drawn to scale.</text>
</svg>
""",
    )


def q17() -> None:
    rows = [
        ("Less than 18 years old", "26%"),
        ("18–40 years old", "21%"),
        ("41–65 years old", "29%"),
        ("Greater than 65 years old", "24%"),
    ]
    x0, y0, c1, c2, rh, hh = 16, 16, 280, 150, 40, 44
    w, h = x0 * 2 + c1 + c2, y0 * 2 + hh + rh * len(rows)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    headers = [("Age group", c1), ("Proportion", c2)]
    x = x0
    for label, cw in headers:
        parts.append(f'<rect x="{x}" y="{y0}" width="{cw}" height="{hh}" fill="#f3f4f6" stroke="#111"/>')
        parts.append(
            f'<text x="{x + cw/2:.1f}" y="{y0 + 28}" text-anchor="middle" {FONT} font-size="15" font-weight="700">{label}</text>'
        )
        x += cw
    for i, (age, prop) in enumerate(rows):
        y = y0 + hh + i * rh
        parts.append(f'<rect x="{x0}" y="{y}" width="{c1}" height="{rh}" fill="#fff" stroke="#111"/>')
        parts.append(
            f'<text x="{x0 + 12}" y="{y + 26}" {FONT} font-size="15">{age}</text>'
        )
        parts.append(f'<rect x="{x0 + c1}" y="{y}" width="{c2}" height="{rh}" fill="#fff" stroke="#111"/>')
        parts.append(
            f'<text x="{x0 + c1 + c2/2:.1f}" y="{y + 26}" text-anchor="middle" {FONT} font-size="15">{prop}</text>'
        )
    parts.append("</svg>")
    write("math1-q17-age-table.svg", "\n".join(parts))


def q20() -> None:
    write(
        "math1-q20-right-triangle.svg",
        f"""
<svg xmlns="http://www.w3.org/2000/svg" width="420" height="280" viewBox="0 0 420 280">
  <rect width="100%" height="100%" fill="#fff"/>
  <polygon points="36,200 320,200 320,36" fill="none" stroke="#111" stroke-width="2.2"/>
  <polyline points="300,200 300,180 320,180" fill="none" stroke="#111" stroke-width="1.6"/>
  <text x="22" y="222" {FONT} font-size="18" font-style="italic">S</text>
  <text x="328" y="222" {FONT} font-size="18" font-style="italic">R</text>
  <text x="328" y="32" {FONT} font-size="18" font-style="italic">Q</text>
  <text x="178" y="222" text-anchor="middle" {FONT} font-size="16">37</text>
  <text x="210" y="262" text-anchor="middle" {FONT} font-size="13">Note: Figure not drawn to scale.</text>
</svg>
""",
    )


if __name__ == "__main__":
    q02()
    q11()
    q14()
    q17()
    q20()
