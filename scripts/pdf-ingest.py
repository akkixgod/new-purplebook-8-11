#!/usr/bin/env python3
"""Render a SAT/EliteXSAT PDF into public/mocks/<slug>/ for agent transcription."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:
    print("Install pymupdf first: py -3 -m pip install pymupdf", file=sys.stderr)
    sys.exit(1)


WATERMARK_RE = re.compile(
    r"El[ijl]+an\s*Ahm[a-z]*|EliteXSAT|Azerba[ij]an|Made in|民心|米|国|长|소",
    re.I,
)


def clean_text(raw: str) -> str:
    lines = []
    for line in raw.splitlines():
        if WATERMARK_RE.search(line) and len(re.sub(WATERMARK_RE, "", line).strip()) < 3:
            continue
        lines.append(line)
    text = "\n".join(lines)
    text = WATERMARK_RE.sub(" ", text)
    text = re.sub(r"[|?]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def ingest(pdf_path: Path, slug: str, scale: float, out_root: Path) -> dict:
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    out_dir = out_root / slug
    pages_dir = out_dir / "pages"
    figures_dir = out_dir / "figures"
    pages_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(pdf_path)
    pages_meta = []
    matrix = pymupdf.Matrix(scale, scale)

    for i, page in enumerate(doc):
        n = i + 1
        png_name = f"page-{n:02d}.png"
        txt_name = f"page-{n:02d}.txt"
        png_path = pages_dir / png_name
        txt_path = pages_dir / txt_name

        pix = page.get_pixmap(matrix=matrix, alpha=False)
        pix.save(str(png_path))

        raw = page.get_text("text")
        cleaned = clean_text(raw)
        txt_path.write_text(cleaned, encoding="utf-8")

        pages_meta.append(
            {
                "page": n,
                "image": f"/mocks/{slug}/pages/{png_name}",
                "text_file": str(txt_path.as_posix()),
                "width": pix.width,
                "height": pix.height,
                "char_count": len(cleaned),
            }
        )
        print(f"page {n:02d}/{doc.page_count}: {pix.width}x{pix.height} chars={len(cleaned)}")

    manifest = {
        "slug": slug,
        "source": str(pdf_path),
        "page_count": doc.page_count,
        "scale": scale,
        "pages": pages_meta,
        "figures_dir": f"/mocks/{slug}/figures",
    }
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {manifest_path}")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="Path to SAT PDF")
    parser.add_argument("--slug", required=True, help="Output folder name under public/mocks/")
    parser.add_argument("--scale", type=float, default=2.0, help="Render scale (default 2.0)")
    parser.add_argument(
        "--out-root",
        type=Path,
        default=Path("public/mocks"),
        help="Mocks root (default public/mocks)",
    )
    args = parser.parse_args()
    ingest(args.pdf.resolve(), args.slug, args.scale, args.out_root.resolve())


if __name__ == "__main__":
    main()
