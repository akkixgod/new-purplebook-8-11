#!/usr/bin/env python3
"""Generate clean SVGs for 2025 March Int-B figures (English Module 1)."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-march-int-b/figures")
OUT.mkdir(parents=True, exist_ok=True)


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
            f'font-family="Georgia, serif" font-size="{title_size}" font-weight="700">{esc(line)}</text>'
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
                f'font-family="Georgia, serif" font-size="11" font-weight="{weight}">{esc(l1)}</text>'
            )
            parts.append(
                f'<text x="{x + w/2}" y="{y + h/2 + 12}" text-anchor="middle" '
                f'font-family="Georgia, serif" font-size="11" font-weight="{weight}">{esc(l2)}</text>'
            )
        else:
            parts.append(
                f'<text x="{x + w/2}" y="{y + h/2 + 4}" text-anchor="middle" '
                f'font-family="Georgia, serif" font-size="{size}" font-weight="{weight}">{esc(text)}</text>'
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


def fta_bar_chart(path: Path) -> None:
    # Values from page-11 (approx on 5-unit grid)
    # Pre-FTA: ES 8.7, MX -1.4, NI 23.6
    # Post-FTA: ES 21.8, MX 13.8, NI 17.7
    tw, th = 720, 420
    left, right, top, bottom = 70, 680, 90, 340
    y_min, y_max = -5, 25
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{th}" viewBox="0 0 {tw} {th}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="{tw/2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">'
        "Average Total Agricultural Export Growth Rate, Five Years</text>",
        f'<text x="{tw/2}" y="48" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">'
        "Pre- and Post-FTA with the United States</text>",
        f'<text x="28" y="{(top+bottom)/2}" text-anchor="middle" font-family="Georgia, serif" font-size="12" '
        'transform="rotate(-90 28 ' + str((top + bottom) / 2) + ')">Growth rate (%)</text>',
        f'<text x="{(left+right)/2}" y="{th-18}" text-anchor="middle" font-family="Georgia, serif" font-size="12">'
        "Export growth</text>",
    ]

    def y_to_px(v: float) -> float:
        return bottom - (v - y_min) / (y_max - y_min) * (bottom - top)

    # axes + grid
    zero = y_to_px(0)
    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#111" stroke-width="1.5"/>')
    parts.append(f'<line x1="{left}" y1="{zero}" x2="{right}" y2="{zero}" stroke="#111" stroke-width="1.5"/>')
    for tick in range(-5, 30, 5):
        yy = y_to_px(tick)
        parts.append(f'<line x1="{left}" y1="{yy}" x2="{right}" y2="{yy}" stroke="#ddd" stroke-width="1"/>')
        parts.append(
            f'<text x="{left-8}" y="{yy+4}" text-anchor="end" font-family="Georgia, serif" font-size="11">{tick}</text>'
        )

    groups = [
        ("Pre-FTA", [8.7, -1.4, 23.6]),
        ("Post-FTA", [21.8, 13.8, 17.7]),
    ]
    colors = ["#4b5563", "#d1d5db", "#111"]  # ES dark gray, MX light gray, NI black
    labels = ["El Salvador (CAFTA-DR)", "Mexico (NAFTA)", "Nicaragua (CAFTA-DR)"]
    group_w = (right - left) / 2
    bar_w = 28
    gap = 8

    for gi, (gname, vals) in enumerate(groups):
        gx = left + gi * group_w + group_w / 2
        start = gx - (3 * bar_w + 2 * gap) / 2
        for bi, val in enumerate(vals):
            x = start + bi * (bar_w + gap)
            y1 = zero
            y2 = y_to_px(val)
            top_y = min(y1, y2)
            h = abs(y2 - y1)
            parts.append(
                f'<rect x="{x}" y="{top_y}" width="{bar_w}" height="{max(h,1)}" fill="{colors[bi]}" stroke="#111" stroke-width="0.5"/>'
            )
        parts.append(
            f'<text x="{gx}" y="{bottom+22}" text-anchor="middle" font-family="Georgia, serif" font-size="12">{gname}</text>'
        )

    # legend
    lx, ly = 480, 70
    for i, lab in enumerate(labels):
        yy = ly + i * 20
        parts.append(f'<rect x="{lx}" y="{yy-10}" width="14" height="14" fill="{colors[i]}" stroke="#111"/>')
        parts.append(
            f'<text x="{lx+20}" y="{yy+2}" font-family="Georgia, serif" font-size="11">{esc(lab)}</text>'
        )

    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")
    print("wrote", path.name)


def main() -> None:
    table_svg(
        OUT / "eng1-q10-africa-population.svg",
        "Population and Population Density of African Countries in 2015",
        ["Country", "Density (inhabitants/km²)", "Area (km²)", "Estimated population"],
        [
            ["São Tomé and Príncipe", "189.8", "1,001", "190,000"],
            ["Ethiopia", "88.2", "1,127,127", "99,391,000"],
            ["Mauritania", "3.9", "1,030,700", "4,068,000"],
            ["Angola", "20.1", "1,246,700", "25,022,000"],
        ],
        [170, 160, 120, 150],
        title_size=12,
    )

    fta_bar_chart(OUT / "eng1-q11-fta-export-growth.svg")

    table_svg(
        OUT / "eng1-q12-lava-worlds.svg",
        "Three Candidate Lava Worlds, by Modeled Mass,\nDensity, and Surface Temperature",
        ["Planet", "Mass (Earth masses)", "Density ratio", "Temperature (kelvins)"],
        [
            ["HD 80653 b", "5.6", "7.4", "2,300"],
            ["Kepler-10 b", "3.6", "6.0", "2,130"],
            ["K2-265 b", "0.8", "7.1", "1,400"],
        ],
        [140, 150, 130, 160],
    )

    table_svg(
        OUT / "eng1-q13-productivity-loss.svg",
        "Average Monetized Productivity Loss at Two Points\nAfter Programs Began, in Australian Dollars",
        ["Type of training", "12 weeks", "12 months"],
        [
            ["EET", "268", "171"],
            ["EHP", "282", "436"],
        ],
        [160, 100, 100],
    )


if __name__ == "__main__":
    main()
