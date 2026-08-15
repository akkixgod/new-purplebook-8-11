#!/usr/bin/env python3
"""Generate English SVG figures for 2025 June US-C."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-june-us-c/figures")
OUT.mkdir(parents=True, exist_ok=True)
FONT = "Georgia, serif"


def write(name: str, svg: str) -> None:
    (OUT / name).write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", name)


def esc(t: object) -> str:
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def table_svg(
    name: str,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_w: list[int],
    title_size: int = 12,
) -> None:
    row_h = 40
    header_h = 56 if any(len(h) > 18 for h in headers) else 36
    title_lines = [ln for ln in title.split("\n") if ln]
    title_block = 16 + len(title_lines) * 17 if title_lines else 12
    tw = sum(col_w) + 40
    th = title_block + header_h + row_h * len(rows) + 20
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{th}" viewBox="0 0 {tw} {th}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for i, line in enumerate(title_lines):
        parts.append(
            f'<text x="{tw/2}" y="{18 + i * 17}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="{title_size}" font-weight="700">{esc(line)}</text>'
        )
    y = title_block
    x0 = 20

    def cell(x, y, w, h, text, header=False):
        fill = "#f3f4f6" if header else "#fff"
        weight = "700" if header else "400"
        size = 10 if len(text) > 22 else 12
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#111"/>'
        )
        if header and len(text) > 24:
            words = text.split()
            mid = max(1, len(words) // 2)
            t1, t2 = " ".join(words[:mid]), " ".join(words[mid:])
            parts.append(
                f'<text x="{x+w/2}" y="{y+h/2-4}" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700">{esc(t1)}</text>'
            )
            parts.append(
                f'<text x="{x+w/2}" y="{y+h/2+10}" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="700">{esc(t2)}</text>'
            )
        else:
            parts.append(
                f'<text x="{x+w/2}" y="{y+h/2+4}" text-anchor="middle" font-family="{FONT}" font-size="{size}" font-weight="{weight}">{esc(text)}</text>'
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
    write(name, "\n".join(parts))


def main() -> None:
    table_svg(
        "eng1-q09-hours-worked.svg",
        "Average Hours Worked per Person per Year in 1950 and 2017",
        ["Country", "1950", "2017", "Change in hours", "Percent change in hours"],
        [
            ["Peru", "2,157", "1,932", "−225", "−10%"],
            ["Canada", "2,209", "1,696", "−513", "−23%"],
            ["Denmark", "2,049", "1,400", "−649", "−32%"],
            ["Finland", "2,053", "1,659", "−394", "−19%"],
        ],
        [100, 80, 80, 120, 140],
    )
    table_svg(
        "eng1-q10-tfa.svg",
        "Percent Change in Average Global Market Prices by Commodity\nin Two Agricultural Trade-Reform Scenarios",
        ["Commodity", "Percent change in TFA scenario", "Percent change in tariff-removal scenario"],
        [
            ["Fruits and vegetables", "−1.50", "+0.04"],
            ["Processed foods", "−1.76", "−1.00"],
            ["Rice", "−0.37", "+1.36"],
            ["Wheat", "−1.35", "+0.45"],
        ],
        [160, 180, 220],
    )
    table_svg(
        "eng1-q11-seigniorage.svg",
        "Value, Cost, and Seigniorage of US Coins by Denomination, 2023",
        [
            "Denomination",
            "Total value of units produced (in millions of dollars)",
            "Gross cost (in millions of dollars)",
            "Seigniorage (in millions of dollars)",
            "Seigniorage per $1 issued (dollars)",
        ],
        [
            ["One-cent", "41.4", "127.4", "−86.0", "−2.08"],
            ["Five-cent", "70.8", "163.4", "−92.6", "−1.31"],
            ["Ten-cent", "266.6", "141.1", "125.5", "0.47"],
            ["Quarter-dollar", "568.4", "264.4", "304.0", "0.53"],
        ],
        [120, 160, 140, 140, 140],
        title_size=11,
    )
    table_svg(
        "eng2-q14-dog-iris-ratings.svg",
        "Average Ratings of Perceived Personality Traits of Dogs\nand Human Willingness to Keep or Interact with Them",
        [
            "Image ID number",
            "Irises",
            "Not friendly (0)—Friendly (5)",
            "Immature (0)—Mature (5)",
            "Would not keep (0)—Would keep (3)",
            "Would not interact with (0)—Would interact with (3)",
        ],
        [
            ["24", "light", "2.67", "4.03", "1.4", "1.7"],
            ["14", "light", "2.11", "3.27", "1.55", "1.85"],
            ["8", "dark", "3.52", "2.91", "1.9", "2.45"],
            ["3", "dark", "3.88", "2.51", "2.35", "2.65"],
        ],
        [90, 70, 130, 120, 130, 150],
        title_size=11,
    )


if __name__ == "__main__":
    main()
