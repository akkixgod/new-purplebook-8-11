#!/usr/bin/env python3
"""Generate clean SVGs for 2025 June Int-B figures."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-june-int-b/figures")
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
    header_h = 48 if any(len(h) > 20 for h in headers) else 36
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


def main() -> None:
    table_svg(
        OUT / "eng2-q12-spider-capes.svg",
        "Spider Attacks on Termites with Different Capes",
        ["Type looked at first", "Solid black", "Solid white", "Black-and-white striped"],
        [
            ["Solid black cape", "60%", "26%", "13%"],
            ["Solid white cape", "14%", "86%", "0%"],
            ["Black-and-white striped cape", "25%", "50%", "25%"],
        ],
        [200, 100, 100, 160],
    )

    # Math1 Q1 function table with fraction
    path = OUT / "math1-q01-function-table.svg"
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="220" height="240" viewBox="0 0 220 240">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<rect x="40" y="20" width="70" height="40" fill="#f3f4f6" stroke="#111"/>',
        '<text x="75" y="46" text-anchor="middle" font-family="Georgia, serif" font-size="16" font-weight="700">x</text>',
        '<rect x="110" y="20" width="70" height="40" fill="#f3f4f6" stroke="#111"/>',
        '<text x="145" y="46" text-anchor="middle" font-family="Georgia, serif" font-size="16" font-weight="700">f(x)</text>',
    ]
    rows = [("-1", None), ("0", "1"), ("1", "50"), ("2", "2,500")]
    y = 60
    for xval, fval in rows:
        parts.append(f'<rect x="40" y="{y}" width="70" height="40" fill="#fff" stroke="#111"/>')
        parts.append(
            f'<text x="75" y="{y+26}" text-anchor="middle" font-family="Georgia, serif" font-size="15">{xval}</text>'
        )
        parts.append(f'<rect x="110" y="{y}" width="70" height="40" fill="#fff" stroke="#111"/>')
        if fval is None:
            # 1/50 as stacked fraction
            parts.append(
                f'<text x="145" y="{y+16}" text-anchor="middle" font-family="Georgia, serif" font-size="13">1</text>'
            )
            parts.append(f'<line x1="130" y1="{y+20}" x2="160" y2="{y+20}" stroke="#111" stroke-width="1"/>')
            parts.append(
                f'<text x="145" y="{y+34}" text-anchor="middle" font-family="Georgia, serif" font-size="13">50</text>'
            )
        else:
            parts.append(
                f'<text x="145" y="{y+26}" text-anchor="middle" font-family="Georgia, serif" font-size="15">{fval}</text>'
            )
        y += 40
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")
    print("wrote", path.name)

    # Parallel lines Q9
    path = OUT / "math1-q09-parallel-lines.svg"
    path.write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" width="420" height="280" viewBox="0 0 420 280">
  <rect width="100%" height="100%" fill="#fff"/>
  <line x1="40" y1="90" x2="340" y2="90" stroke="#111" stroke-width="2"/>
  <text x="350" y="95" font-family="Georgia, serif" font-size="16">r</text>
  <line x1="40" y1="180" x2="340" y2="180" stroke="#111" stroke-width="2"/>
  <text x="350" y="185" font-family="Georgia, serif" font-size="16">s</text>
  <line x1="120" y1="220" x2="280" y2="50" stroke="#111" stroke-width="2"/>
  <text x="290" y="48" font-family="Georgia, serif" font-size="16">t</text>
  <path d="M 210 90 L 228 90 A 18 18 0 0 0 218 74" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="235" y="78" font-family="Georgia, serif" font-size="14">x°</text>
  <path d="M 168 180 L 186 180 A 18 18 0 0 0 176 164" fill="none" stroke="#111" stroke-width="1.5"/>
  <text x="192" y="168" font-family="Georgia, serif" font-size="14">44°</text>
  <text x="210" y="255" text-anchor="middle" font-family="Georgia, serif" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>
""",
        encoding="utf-8",
    )
    print("wrote", path.name)

    # Newsletter exponential Q17
    path = OUT / "math1-q17-newsletter-graph.svg"
    # y = 300 * 2^x ; map x:0-4 -> px, y:0-1400 -> py
    def px(x: float) -> float:
        return 60 + x * 70

    def py(y: float) -> float:
        return 260 - (y / 1400) * 220

    pts = [(x, 300 * (2**x)) for x in [i / 20 for i in range(0, 75)]]
    pts = [(px(x), py(y)) for x, y in pts if y <= 1400]
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    labels_y = [400, 800, 1200]
    path.write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">
  <rect width="100%" height="100%" fill="#fff"/>
  <line x1="60" y1="260" x2="360" y2="260" stroke="#111" stroke-width="1.5"/>
  <line x1="60" y1="260" x2="60" y2="30" stroke="#111" stroke-width="1.5"/>
  <text x="370" y="265" font-family="Georgia, serif" font-size="14">x</text>
  <text x="48" y="28" font-family="Georgia, serif" font-size="14">y</text>
  <text x="52" y="268" text-anchor="end" font-family="Georgia, serif" font-size="12">O</text>
  {"".join(f'<line x1="{px(i)}" y1="260" x2="{px(i)}" y2="265" stroke="#111"/><text x="{px(i)}" y="280" text-anchor="middle" font-family="Georgia, serif" font-size="12">{i}</text>' for i in range(1,5))}
  {"".join(f'<line x1="55" y1="{py(v)}" x2="60" y2="{py(v)}" stroke="#111"/><text x="50" y="{py(v)+4}" text-anchor="end" font-family="Georgia, serif" font-size="11">{v:,}</text>' for v in labels_y)}
  <path d="{d}" fill="none" stroke="#111" stroke-width="2"/>
</svg>
""",
        encoding="utf-8",
    )
    print("wrote", path.name)

    table_svg(
        OUT / "math1-q18-groups-table.svg",
        "",
        ["Group", "Number of objects"],
        [["A", "325"], ["B", "64"], ["C", "611"], ["D", "96"], ["Total", "1,096"]],
        [100, 160],
    )

    # Line k Q20
    path = OUT / "math1-q20-line-k.svg"
    # map -10..10 to px
    def gx(x: float) -> float:
        return 200 + x * 16

    def gy(y: float) -> float:
        return 200 - y * 16

    # line through (-2,2) and (2,-3): y = -1.25x - 0.5
    x1, x2 = -9, 9
    y1 = -1.25 * x1 - 0.5
    y2 = -1.25 * x2 - 0.5
    grid = []
    for i in range(-10, 11):
        grid.append(f'<line x1="{gx(i)}" y1="{gy(-10)}" x2="{gx(i)}" y2="{gy(10)}" stroke="#e5e7eb"/>')
        grid.append(f'<line x1="{gx(-10)}" y1="{gy(i)}" x2="{gx(10)}" y2="{gy(i)}" stroke="#e5e7eb"/>')
    ticks = []
    for i in range(-10, 11, 2):
        if i == 0:
            continue
        ticks.append(
            f'<text x="{gx(i)}" y="{gy(0)+14}" text-anchor="middle" font-family="Georgia, serif" font-size="10">{i}</text>'
        )
        ticks.append(
            f'<text x="{gx(0)-10}" y="{gy(i)+4}" text-anchor="middle" font-family="Georgia, serif" font-size="10">{i}</text>'
        )
    path.write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(grid)}
  <line x1="{gx(-10)}" y1="{gy(0)}" x2="{gx(10)}" y2="{gy(0)}" stroke="#111" stroke-width="1.5"/>
  <line x1="{gx(0)}" y1="{gy(-10)}" x2="{gx(0)}" y2="{gy(10)}" stroke="#111" stroke-width="1.5"/>
  {"".join(ticks)}
  <line x1="{gx(x1)}" y1="{gy(y1)}" x2="{gx(x2)}" y2="{gy(y2)}" stroke="#111" stroke-width="2"/>
  <circle cx="{gx(-2)}" cy="{gy(2)}" r="3.5" fill="#111"/>
  <circle cx="{gx(2)}" cy="{gy(-3)}" r="3.5" fill="#111"/>
  <text x="{gx(-6)}" y="{gy(7)-8}" font-family="Georgia, serif" font-size="14">k</text>
</svg>
""",
        encoding="utf-8",
    )
    print("wrote", path.name)

    table_svg(
        OUT / "math1-q21-r-table.svg",
        "",
        ["x", "r(x)"],
        [["−41", "−6"], ["−21", "0"], ["−1", "6"]],
        [80, 80],
    )

    print("done")


if __name__ == "__main__":
    main()
