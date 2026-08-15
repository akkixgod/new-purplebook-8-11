#!/usr/bin/env python3
"""Generate clean SVG tables for 2025 June Int-A English figures."""

from pathlib import Path

OUT = Path("public/mocks/2025-june-int-a/figures")
OUT.mkdir(parents=True, exist_ok=True)


def esc(t: str) -> str:
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def table_svg(
    path: Path,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_w: list[int],
    title_size: int = 14,
) -> None:
    row_h = 40
    header_h = 48 if any(len(h) > 22 for h in headers) else 36
    title_lines = title.split("\n")
    title_block = 22 + len(title_lines) * 18
    tw = sum(col_w) + 40
    th = title_block + header_h + row_h * len(rows) + 24
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{th}" viewBox="0 0 {tw} {th}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for i, line in enumerate(title_lines):
        parts.append(
            f'<text x="{tw/2}" y="{22 + i * 18}" text-anchor="middle" '
            f'font-family="Georgia, serif" font-size="{title_size}" font-weight="700">{esc(line)}</text>'
        )
    y = title_block
    x0 = 20

    def cell(x: float, y: float, w: float, h: float, text: str, header: bool = False) -> None:
        fill = "#f3f4f6" if header else "#fff"
        weight = "700" if header else "400"
        size = 11 if header and len(text) > 24 else (12 if len(text) > 28 else 13)
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#111" stroke-width="1"/>'
        )
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
    print("wrote", path)


def main() -> None:
    table_svg(
        OUT / "eng1-q11-hydroelectric-plants.svg",
        "US Hydroelectric Power Plants, 2019",
        ["Plant", "State", "Mode", "Generators", "Avg power (MWh/yr)", "Water source"],
        [
            ["J. Woodruff", "Florida", "peaking", "3", "193,864", "Lake Seminole Res."],
            ["Superior Falls", "Michigan", "run-of-river", "2", "10,693", "Montreal River"],
            ["Norway", "Indiana", "run-of-river", "4", "19,751", "Tippecanoe River"],
            ["White River", "Wisconsin", "run-of-river", "2", "3,999", "White River"],
        ],
        [120, 95, 110, 95, 145, 150],
    )

    table_svg(
        OUT / "eng1-q13-orangutan-peering.svg",
        "Peering at Adult Orangutans by Immature Orangutans",
        ["Individual", "Site", "Sex", "Peering events", "Prop. at permanent residents"],
        [
            ["1", "Suaq", "female", "17", "0.59"],
            ["13", "Tuanan", "male", "27", "0.15"],
            ["15", "Tuanan", "male", "15", "0.00"],
            ["6", "Tuanan", "female", "6", "0.67"],
        ],
        [95, 90, 80, 120, 210],
    )

    table_svg(
        OUT / "eng2-q11-indonesia-renewable.svg",
        "Electricity Capacity Trends (MW) for Four Renewable\nTechnologies in Indonesia (2017–2020)",
        ["Energy", "2017", "2018", "2019", "2020"],
        [
            ["Geothermal", "1,808", "1,948", "2,131", "2,131"],
            ["Renewable hydropower", "5,703", "5,773", "5,976", "6,141"],
            ["Solar", "97.4", "65.5", "155", "185.3"],
            ["Wind", "1.5", "143.5", "154.3", "154.3"],
        ],
        [190, 90, 90, 90, 90],
    )


if __name__ == "__main__":
    main()
