"""Generate Reading & Writing Module 2 figures for the 2025-march-int-c mock.

Only one figure is needed: the Q10 Chesapeake Bay seagrass line graph (PDF page 37).

    py -3 scripts/generate-figures-2025-march-int-c-rw2.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "mocks" / "2025-march-int-c" / "figures"

FONT = "Georgia, serif"

YEARS = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
EELGRASS = [5400, 7000, 7000, 8600, 8800, 8600, 9700, 5000]
WIDGEON = [5800, 8400, 12400, 15600, 17300, 18000, 16300, 8900]
TOTAL = [19600, 24400, 30500, 37500, 40500, 42600, 43900, 27000]

LEFT, RIGHT, TOP, BOTTOM = 112, 604, 52, 300
YMAX = 45000
YTICKS = [0, 9000, 18000, 27000, 36000, 45000]


def xpos(i):
    step = (RIGHT - LEFT) / len(YEARS)
    return LEFT + (i + 0.5) * step


def ypos(v):
    return BOTTOM - (v / YMAX) * (BOTTOM - TOP)


def marker_circle(x, y):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#fff" stroke="#111" stroke-width="2"/>'


def marker_square(x, y):
    return (
        f'<rect x="{x - 5.5:.1f}" y="{y - 5.5:.1f}" width="11" height="11" '
        f'fill="#b9b9b9" stroke="#111" stroke-width="1.5"/>'
    )


def marker_triangle(x, y):
    pts = f"{x:.1f},{y - 6.5:.1f} {x + 6.5:.1f},{y + 5.0:.1f} {x - 6.5:.1f},{y + 5.0:.1f}"
    return f'<polygon points="{pts}" fill="#111"/>'


def series(values, dash, marker):
    pts = " ".join(f"{xpos(i):.1f},{ypos(v):.1f}" for i, v in enumerate(values))
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    out = [
        f'<polyline points="{pts}" fill="none" stroke="#111" stroke-width="2"{dash_attr}/>'
    ]
    out += [marker(xpos(i), ypos(v)) for i, v in enumerate(values)]
    return out


def build():
    p = []
    p.append(
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="470" viewBox="0 0 640 470">'
    )
    p.append('<rect width="100%" height="100%" fill="#fff"/>')
    p.append(
        f'<text x="320" y="26" text-anchor="middle" font-family="{FONT}" '
        'font-size="15" font-weight="700">Chesapeake Bay Seagrass Coverage 2012\u20132019</text>'
    )

    # Grid
    for t in YTICKS:
        y = ypos(t)
        p.append(
            f'<line x1="{LEFT}" y1="{y:.1f}" x2="{RIGHT}" y2="{y:.1f}" stroke="#111" stroke-width="1"/>'
        )
        p.append(
            f'<text x="{LEFT - 10}" y="{y + 5:.1f}" text-anchor="end" font-family="{FONT}" '
            f'font-size="13">{t:,}</text>'
        )
    for i in range(len(YEARS)):
        x = xpos(i)
        p.append(
            f'<line x1="{x:.1f}" y1="{TOP}" x2="{x:.1f}" y2="{BOTTOM}" stroke="#111" stroke-width="1"/>'
        )
    p.append(
        f'<line x1="{LEFT}" y1="{TOP}" x2="{LEFT}" y2="{BOTTOM}" stroke="#111" stroke-width="1.5"/>'
    )
    p.append(
        f'<line x1="{LEFT}" y1="{BOTTOM}" x2="{RIGHT}" y2="{BOTTOM}" stroke="#111" stroke-width="1.5"/>'
    )

    # Axis titles
    p.append(
        f'<text x="34" y="{(TOP + BOTTOM) / 2:.1f}" text-anchor="middle" font-family="{FONT}" '
        f'font-size="14" transform="rotate(-90 34 {(TOP + BOTTOM) / 2:.1f})">Seagrass area (hectares)</text>'
    )
    for i, yr in enumerate(YEARS):
        x = xpos(i)
        p.append(
            f'<text x="{x:.1f}" y="{BOTTOM + 22:.1f}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="13" transform="rotate(-40 {x:.1f} {BOTTOM + 22:.1f})">{yr}</text>'
        )
    p.append(
        f'<text x="{(LEFT + RIGHT) / 2:.1f}" y="{BOTTOM + 72:.1f}" text-anchor="middle" '
        f'font-family="{FONT}" font-size="14">Year</text>'
    )

    # Series: eelgrass (solid + triangles), widgeon (dashed + squares), total (dotted + circles)
    p += series(TOTAL, "3 6", marker_circle)
    p += series(WIDGEON, "11 7", marker_square)
    p += series(EELGRASS, None, marker_triangle)

    # Legend
    lx, ly = 178, 388
    p.append(
        f'<rect x="{lx}" y="{ly}" width="284" height="70" fill="#fff" stroke="#111" stroke-width="1"/>'
    )
    rows = [
        ("eelgrass", None, marker_triangle),
        ("widgeon grass", "11 7", marker_square),
        ("total of all types of seagrass", "3 6", marker_circle),
    ]
    for i, (label, dash, marker) in enumerate(rows):
        y = ly + 18 + i * 20
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        p.append(
            f'<line x1="{lx + 14}" y1="{y:.1f}" x2="{lx + 62}" y2="{y:.1f}" stroke="#111" '
            f'stroke-width="2"{dash_attr}/>'
        )
        p.append(marker(lx + 38, y))
        p.append(
            f'<text x="{lx + 76}" y="{y + 5:.1f}" font-family="{FONT}" font-size="13">{label}</text>'
        )

    p.append("</svg>")
    return "\n".join(p)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "eng2-q10-chesapeake-seagrass.svg"
    path.write_text(build(), encoding="utf-8")
    print("wrote", path)


if __name__ == "__main__":
    main()
