"""Generate Reading & Writing Module 2 figures for the 2025-march-int-e mock.

    py -3 scripts/generate-figures-2025-march-int-e-rw2.py

Figures:
  Q11 stony-coral depth table (PDF page 38)
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "mocks" / "2025-march-int-e" / "figures"

FONT = "Georgia, serif"


def esc(t: object) -> str:
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def table_svg(
    path: Path,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_w: list[int],
    title_size: int = 13,
    italic_col: int | None = 0,
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

    def cell(x: float, y: float, w: float, h: float, text: str, header: bool = False, italic: bool = False) -> None:
        fill = "#f3f4f6" if header else "#fff"
        weight = "700" if header else "400"
        size = 11 if len(text) > 28 else 12
        style = " font-style=\"italic\"" if italic and not header else ""
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
                f'font-family="{FONT}" font-size="{size}" font-weight="{weight}"{style}>{esc(text)}</text>'
            )

    x = x0
    for i, h in enumerate(headers):
        cell(x, y, col_w[i], header_h, h, True)
        x += col_w[i]
    y += header_h
    for r in rows:
        x = x0
        for i, val in enumerate(r):
            cell(x, y, col_w[i], row_h, val, False, italic=(i == italic_col))
            x += col_w[i]
        y += row_h
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")
    print("wrote", path.name)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    table_svg(
        OUT / "eng2-q11-coral-depths.svg",
        "Minimum and Maximum Depths of Stony Coral Species in\nCaribbean and Indo-Pacific Waters",
        ["Species", "Minimum depth (meters)", "Maximum depth (meters)"],
        [
            ["Psammocora albopicta", "1", "28"],
            ["Agaricia grahamae", "20", "115"],
            ["Astreopora gracilis", "5", "15"],
            ["Acropora echinata", "8", "25"],
        ],
        [220, 180, 180],
    )


if __name__ == "__main__":
    main()
