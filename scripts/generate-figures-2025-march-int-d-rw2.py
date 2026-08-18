"""Generate Reading & Writing Module 2 figures for the 2025-march-int-d mock.

    py -3 scripts/generate-figures-2025-march-int-d-rw2.py

Figures:
  Q9  Chesapeake Bay seagrass line graph (PDF page 34)
  Q10 migrating-animal travel-distance table (PDF page 35)
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "mocks" / "2025-march-int-d" / "figures"

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


def build_seagrass():
    p = []
    p.append(
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="470" viewBox="0 0 640 470">'
    )
    p.append('<rect width="100%" height="100%" fill="#fff"/>')
    p.append(
        f'<text x="320" y="26" text-anchor="middle" font-family="{FONT}" '
        'font-size="15" font-weight="700">Chesapeake Bay Seagrass Coverage 2012\u20132019</text>'
    )

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

    p += series(TOTAL, "3 6", marker_circle)
    p += series(WIDGEON, "11 7", marker_square)
    p += series(EELGRASS, None, marker_triangle)

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


def esc(t: object) -> str:
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def table_svg(
    path: Path,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_w: list[int],
    title_size: int = 13,
) -> None:
    row_h = 40
    header_h = 52 if any(len(h) > 18 for h in headers) else 36
    title_lines = [ln for ln in title.split("\n") if ln]
    title_block = 18 + len(title_lines) * 18 if title_lines else 12
    tw = sum(col_w) + 40
    th = title_block + header_h + row_h * len(rows) + 24
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{th}" viewBox="0 0 {tw} {th}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for i, line in enumerate(title_lines):
        parts.append(
            f'<text x="{tw/2}" y="{20 + i * 18}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="{title_size}" font-weight="700">{esc(line)}</text>'
        )
    y = title_block
    x0 = 20

    def cell(x: float, y: float, w: float, h: float, text: str, header: bool = False) -> None:
        fill = "#f3f4f6" if header else "#fff"
        weight = "700" if header else "400"
        size = 11 if len(text) > 28 else 12
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#111" stroke-width="1"/>'
        )
        if header and len(text) > 22:
            words = text.split()
            mid = (len(words) + 1) // 2
            l1 = " ".join(words[:mid])
            l2 = " ".join(words[mid:])
            parts.append(
                f'<text x="{x + w/2}" y="{y + h/2 - 4}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="11" font-weight="{weight}">{esc(l1)}</text>'
            )
            parts.append(
                f'<text x="{x + w/2}" y="{y + h/2 + 12}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="11" font-weight="{weight}">{esc(l2)}</text>'
            )
        else:
            parts.append(
                f'<text x="{x + w/2}" y="{y + h/2 + 4}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="{size}" font-weight="{weight}">{esc(text)}</text>'
            )

    x = x0
    for i, h in enumerate(headers):
        cell(x, y, col_w[i], header_h, h, True)
        x += col_w[i]
    y += header_h
    for r in rows:
        x = x0
        for i, val in enumerate(r):
            cell(x, y, col_w[i], row_h, val, False)
            x += col_w[i]
        y += row_h
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")
    print("wrote", path.name)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    seagrass = OUT / "eng2-q09-chesapeake-seagrass.svg"
    seagrass.write_text(build_seagrass(), encoding="utf-8")
    print("wrote", seagrass.name)

    table_svg(
        OUT / "eng2-q10-migration-distances.svg",
        "Reported Annual Travel Distances in Four Studies of\nMigrating Animal Populations",
        ["Species", "Continent", "Distance (km)", "Measurement method"],
        [
            ["Brown bear", "North America", "1,325", "GPS"],
            ["Tibetan antelope", "Asia", "700", "RTD"],
            ["Caribou", "North America", "4,868", "GPS"],
            ["Reindeer", "Asia", "1,200", "RTD"],
        ],
        [160, 140, 140, 180],
    )


if __name__ == "__main__":
    main()
