#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2025 June US-C Math Module 2."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-june-us-c/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Georgia, serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def table_svg(
    headers: tuple[str, str],
    rows: list[tuple[str, str]],
    *,
    col_widths: tuple[int, int] = (80, 80),
    cell_h: int = 40,
) -> str:
    ox, oy = 24, 16
    w0, w1 = col_widths
    width = ox * 2 + w0 + w1
    height = oy * 2 + cell_h * (len(rows) + 1)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for i, label in enumerate(headers):
        x = ox + (0 if i == 0 else w0)
        ww = w0 if i == 0 else w1
        parts.append(
            f'<rect x="{x}" y="{oy}" width="{ww}" height="{cell_h}" fill="#f3f4f6" stroke="#111"/>'
        )
        parts.append(
            f'<text x="{x + ww / 2}" y="{oy + 26}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="15" font-weight="700">{label}</text>'
        )
    for r, (a, b) in enumerate(rows):
        y = oy + cell_h * (r + 1)
        for i, val in enumerate((a, b)):
            x = ox + (0 if i == 0 else w0)
            ww = w0 if i == 0 else w1
            parts.append(
                f'<rect x="{x}" y="{y}" width="{ww}" height="{cell_h}" fill="#fff" stroke="#111"/>'
            )
            parts.append(
                f'<text x="{x + ww / 2}" y="{y + 26}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="15">{val}</text>'
            )
    parts.append("</svg>")
    return "\n".join(parts)


def math2_q13_xy_table() -> str:
    return table_svg(
        ("x", "y"),
        [("-6", "-14"), ("-3", "-16"), ("3", "-20"), ("6", "-22")],
    )


def math2_q19_mail_table() -> str:
    return table_svg(
        ("Pieces of mail", "Days"),
        [
            ("0", "2"),
            ("4", "2"),
            ("5", "2"),
            ("6", "2"),
            ("7", "1"),
            ("8", "1"),
            ("17", "1"),
        ],
        col_widths=(140, 80),
    )


def main() -> None:
    write("math2-q13-xy-table.svg", math2_q13_xy_table())
    write("math2-q19-mail-table.svg", math2_q19_mail_table())
    print("done")


if __name__ == "__main__":
    main()
