#!/usr/bin/env python3
"""Generate R&W Module 2 SVG figures for PurpleBook test 10."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/purplebook-test-10/figures")
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def eng2_q10_national_parks() -> str:
    """Line graph: recreation visits to four US national parks, peak season 2021."""
    W, H = 620, 460
    pad_l, pad_r, pad_t, pad_b = 70, 30, 70, 110
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    y_max = 1100
    months = ["June", "July", "August"]
    # Approximate values (thousands of visitors) matching College Board graph
    series = {
        "Yellowstone": {"vals": [940, 1080, 920], "dash": None, "marker": "triangle"},
        "Rocky Mountain": {"vals": [670, 900, 750], "dash": None, "marker": "diamond"},
        "Zion": {"vals": [680, 590, 460], "dash": "6 4", "marker": "circle"},
        "Grand Canyon": {"vals": [540, 560, 480], "dash": "2 3", "marker": "square"},
    }

    def sx(i: int) -> float:
        return pad_l + (i + 0.5) * (plot_w / 3)

    def sy(v: float) -> float:
        return pad_t + plot_h - (v / y_max) * plot_h

    parts: list[str] = [
        f'<text x="{W/2}" y="28" text-anchor="middle" font-family="Georgia, serif" '
        f'font-size="13" font-weight="700">Recreation Visits by Month to Four US National Parks</text>',
        f'<text x="{W/2}" y="48" text-anchor="middle" font-family="Georgia, serif" '
        f'font-size="12" font-weight="700">during the Peak Season in 2021</text>',
        f'<text x="18" y="{(pad_t + pad_t + plot_h) / 2}" text-anchor="middle" '
        f'font-family="Georgia, serif" font-size="11" '
        f'transform="rotate(-90 18 {(pad_t + pad_t + plot_h) / 2})">'
        f"Number of recreation visits</text>",
        f'<text x="34" y="{(pad_t + pad_t + plot_h) / 2 + 90}" text-anchor="middle" '
        f'font-family="Georgia, serif" font-size="10" '
        f'transform="rotate(-90 34 {(pad_t + pad_t + plot_h) / 2 + 90})">'
        f"(in thousands of visitors)</text>",
    ]
    for v in range(0, 1101, 100):
        y = sy(v)
        parts.append(
            f'<line x1="{pad_l}" y1="{y}" x2="{W - pad_r}" y2="{y}" stroke="#e5e7eb"/>'
            f'<text x="{pad_l - 8}" y="{y + 4}" text-anchor="end" '
            f'font-family="Georgia, serif" font-size="11">{v}</text>'
        )
    parts.append(
        f'<rect x="{pad_l}" y="{pad_t}" width="{plot_w}" height="{plot_h}" '
        f'fill="none" stroke="#111"/>'
    )
    for i, m in enumerate(months):
        parts.append(
            f'<text x="{sx(i)}" y="{pad_t + plot_h + 22}" text-anchor="middle" '
            f'font-family="Georgia, serif" font-size="12">{m}</text>'
        )
    parts.append(
        f'<text x="{W/2}" y="{pad_t + plot_h + 44}" text-anchor="middle" '
        f'font-family="Georgia, serif" font-size="12">Month</text>'
    )

    for name, meta in series.items():
        pts = " ".join(f"{sx(i)},{sy(v)}" for i, v in enumerate(meta["vals"]))
        dash = f' stroke-dasharray="{meta["dash"]}"' if meta["dash"] else ""
        parts.append(
            f'<polyline points="{pts}" fill="none" stroke="#111" stroke-width="2"{dash}/>'
        )
        for i, v in enumerate(meta["vals"]):
            x, y = sx(i), sy(v)
            mk = meta["marker"]
            if mk == "triangle":
                parts.append(
                    f'<polygon points="{x},{y - 6} {x - 5.5},{y + 5} {x + 5.5},{y + 5}" fill="#111"/>'
                )
            elif mk == "diamond":
                parts.append(
                    f'<polygon points="{x},{y - 6} {x + 6},{y} {x},{y + 6} {x - 6},{y}" '
                    f'fill="#fff" stroke="#111" stroke-width="1.5"/>'
                )
            elif mk == "circle":
                parts.append(
                    f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="#111" stroke-width="1.5"/>'
                )
            else:
                parts.append(
                    f'<rect x="{x - 4}" y="{y - 4}" width="8" height="8" '
                    f'fill="#111" stroke="#111"/>'
                )

    # Legend
    ly = H - 28
    legend = [
        ("Yellowstone", "triangle", None, 70),
        ("Rocky Mountain", "diamond", None, 210),
        ("Zion", "circle", "6 4", 370),
        ("Grand Canyon", "square", "2 3", 480),
    ]
    for label, mk, dash, lx in legend:
        if dash:
            parts.append(
                f'<line x1="{lx}" y1="{ly}" x2="{lx + 28}" y2="{ly}" stroke="#111" '
                f'stroke-width="2" stroke-dasharray="{dash}"/>'
            )
        else:
            parts.append(
                f'<line x1="{lx}" y1="{ly}" x2="{lx + 28}" y2="{ly}" stroke="#111" stroke-width="2"/>'
            )
        cx, cy = lx + 14, ly
        if mk == "triangle":
            parts.append(
                f'<polygon points="{cx},{cy - 5} {cx - 4.5},{cy + 4} {cx + 4.5},{cy + 4}" fill="#111"/>'
            )
        elif mk == "diamond":
            parts.append(
                f'<polygon points="{cx},{cy - 5} {cx + 5},{cy} {cx},{cy + 5} {cx - 5},{cy}" '
                f'fill="#fff" stroke="#111" stroke-width="1.5"/>'
            )
        elif mk == "circle":
            parts.append(
                f'<circle cx="{cx}" cy="{cy}" r="4" fill="#fff" stroke="#111" stroke-width="1.5"/>'
            )
        else:
            parts.append(
                f'<rect x="{cx - 3.5}" y="{cy - 3.5}" width="7" height="7" fill="#111"/>'
            )
        parts.append(
            f'<text x="{lx + 34}" y="{ly + 4}" font-family="Georgia, serif" font-size="11">{label}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def eng2_q11_tribal_nations() -> str:
    """Table: total areas of five tribal nations (same data as PB4 eng2-q11)."""
    title = "Total Areas of Five Tribal Nations around the United States"
    headers = ["Tribal nation", "Location", "Area (square miles)"]
    rows = [
        ["Crow Tribe", "Montana", "3,606"],
        ["White Earth Nation", "Minnesota", "1,167"],
        ["Tohono O'odham Nation", "Arizona", "4,453"],
        ["Choctaw Nation", "Oklahoma", "10,864"],
        ["Yakama Nation", "Washington", "2,188"],
    ]
    widths = [200, 120, 140]
    row_h = 36
    font_size = 11
    width = sum(widths) + 40
    title_h = 56
    height = title_h + 20 + row_h * (1 + len(rows)) + 16
    x0, y0 = 20, title_h
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{row_h}" fill="#f3f4f6" stroke="#111"/>'
            f'<text x="{x + widths[i]/2}" y="{y0 + 24}" text-anchor="middle" '
            f'font-family="Georgia, serif" font-size="{font_size}" font-weight="700">{h}</text>'
        )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + row_h * (r + 1)
        x = x0
        for i, cell in enumerate(row):
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i]/2}" y="{y + 24}" text-anchor="middle" '
                f'font-family="Georgia, serif" font-size="{font_size}">{cell}</text>'
            )
            x += widths[i]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  <text x="{width/2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="700">{title}</text>
  {"".join(cells)}
</svg>'''


if __name__ == "__main__":
    write("eng2-q10-national-parks.svg", eng2_q10_national_parks())
    write("eng2-q11-tribal-nations.svg", eng2_q11_tribal_nations())
