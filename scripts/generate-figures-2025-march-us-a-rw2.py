"""Generate Reading & Writing Module 2 figures for the 2025-march-us-a mock.

    py -3 scripts/generate-figures-2025-march-us-a-rw2.py

Figures:
  Q9  stony-coral depth table (PDF pages 45 / 47)
  Q11 Story Rating: Spoiled vs. Unspoiled bar graph (PDF page 49)
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "mocks" / "2025-march-us-a" / "figures"

FONT = "Georgia, serif"


def esc(t: object) -> str:
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write(path: Path, parts: list[str]) -> None:
    path.write_text("\n".join(parts), encoding="utf-8")
    print("wrote", path.name)


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
        style = ' font-style="italic"' if italic and not header else ""
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
    write(path, parts)


def story_rating() -> None:
    stories = [
        ("A Dark Brown Dog", 3.5, 4.6),
        ("Owl Creek Bridge", 4.9, 5.1),
        ("Blitzed", 6.2, 7.1),
        ("A Chess Problem", 6.1, 7.2),
        ("The Calm", 4.3, 5.0),
        ("Plumbing", 4.1, 4.9),
    ]
    tw, th = 720, 420
    left, bottom, top, right = 70, 340, 50, 680
    plot_h = bottom - top
    plot_w = right - left
    ymax = 8
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{th}" viewBox="0 0 {tw} {th}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<text x="{(left+right)/2}" y="28" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="700">Story Rating: Spoiled vs. Unspoiled</text>',
        f'<text x="22" y="{(top+bottom)/2}" text-anchor="middle" transform="rotate(-90 22 {(top+bottom)/2})" font-family="{FONT}" font-size="11">Average enjoyment rating (1 = lowest; 10 = highest)</text>',
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#111"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#111"/>',
    ]
    for yv in range(0, 9):
        yy = bottom - (yv / ymax) * plot_h
        parts.append(f'<line x1="{left}" y1="{yy}" x2="{right}" y2="{yy}" stroke="#e5e7eb"/>')
        parts.append(
            f'<text x="{left-8}" y="{yy+4}" text-anchor="end" font-family="{FONT}" font-size="11">{yv}</text>'
        )
    group_w = plot_w / len(stories)
    bar_w = group_w * 0.32
    for i, (name, unsp, spo) in enumerate(stories):
        cx = left + (i + 0.5) * group_w
        x1 = cx - bar_w - 2
        x2 = cx + 2
        h1 = (unsp / ymax) * plot_h
        h2 = (spo / ymax) * plot_h
        parts.append(
            f'<rect x="{x1}" y="{bottom-h1}" width="{bar_w}" height="{h1}" fill="#d1d5db" stroke="#111"/>'
        )
        parts.append(
            f'<rect x="{x2}" y="{bottom-h2}" width="{bar_w}" height="{h2}" fill="#4b5563" stroke="#111"/>'
        )
        parts.append(
            f'<text x="{cx}" y="{bottom+12}" text-anchor="end" transform="rotate(-35 {cx} {bottom+12})" '
            f'font-family="{FONT}" font-size="10">"{esc(name)}"</text>'
        )
    parts.append('<rect x="560" y="48" width="14" height="14" fill="#d1d5db" stroke="#111"/>')
    parts.append(f'<text x="580" y="60" font-family="{FONT}" font-size="12">unspoiled</text>')
    parts.append('<rect x="560" y="70" width="14" height="14" fill="#4b5563" stroke="#111"/>')
    parts.append(f'<text x="580" y="82" font-family="{FONT}" font-size="12">spoiled</text>')
    parts.append(f'<text x="360" y="400" text-anchor="middle" font-family="{FONT}" font-size="12">Story</text>')
    parts.append("</svg>")
    write(OUT / "eng2-q11-story-rating.svg", parts)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    table_svg(
        OUT / "eng2-q09-coral-depths.svg",
        "Minimum and Maximum Depths of Stony Coral Species in\nCaribbean and Indo-Pacific Waters",
        ["Species", "Minimum depth (meters)", "Maximum depth (meters)"],
        [
            ["Agaricia grahamae", "20", "115"],
            ["Acropora striata", "10", "25"],
            ["Danafungia scruposa", "1", "27"],
            ["Acropora anthocercis", "5", "10"],
        ],
        [220, 180, 180],
    )
    story_rating()


if __name__ == "__main__":
    main()
